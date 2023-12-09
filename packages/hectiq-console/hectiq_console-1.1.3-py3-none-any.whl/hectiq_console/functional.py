from hectiq_console import CONSOLE_APP_URL

import os
import contextvars 
import requests
import time
import datetime as dt
from typing import Optional, Union, List, Dict, Literal
from contextlib import contextmanager
import logging
logger = logging.getLogger(__name__)

resource_cvar = contextvars.ContextVar("resource_id", default=None) 
api_key_cvar = contextvars.ContextVar("api_key", default=None) 
organization_cvar = contextvars.ContextVar("organization", default=None)
current_job_cvar = contextvars.ContextVar("current_job", default=None)
current_job_step_cvar = contextvars.ContextVar("current_job_step", default=None)
batch_annotations_cvar = contextvars.ContextVar("batch_annotations", default=None)

def set_ressource(resource: str):
    """Will be removed in the future. Use `set_resource` instead."""
    resource_cvar.set(resource)

def set_resource(resource: str):
    resource_cvar.set(resource)

def set_organization(organization: str):
    organization_cvar.set(organization)

def set_job(job: str):
    current_job_cvar.set(job)

def get_job() -> Optional[str]:
    return current_job_cvar.get()

def set_job_step(job_step: str):
    current_job_step_cvar.set(job_step)

def get_job_step() -> Optional[str]:
    return current_job_step_cvar.get()

def get_organization() -> Optional[str]:
    """Get the organization in the context.

    Returns:
        str: Organization
    """
    return organization_cvar.get()

def get_resource(resource: Optional[str] = None) -> Optional[str]:
    """Get a resource in the context.

    Args:
        resource (Optional[str], optional): Ressource ID of the resource to get. Defaults to None.

    Returns:
        dict: Ressource object
    """
    if resource is None:
        resource = resource_cvar.get()
    if resource is None:
        raise ValueError("You must provide a resource ID to the get_resource method or use `set_rssource`.")
    return resource

def authenticate(api_key: Optional[str] = None,
                 organization: Optional[str] = None) -> bool:
    """Authenticate to the Hectiq Console.
    If api_key is None, the api_key is taken from:
     - the environment variable `HECTIQ_CONSOLE_API_KEY`.
     - the api_key located in the file `~/.hectiq-console/credentials.toml` (or the HECTIQ_CONSOLE_CREDENTIALS_FILE).

    Args:
        api_key (Optional[str], optional): API key. Defaults to None.
        organization (Optional[str], optional): Organization. Defaults to None. If None, the organization is taken from the context (set with `set_organization`). If None and no organization is set in the context, the first organization is used. If None and no organization is set in the context and the credentials file contains only one organization, this organization is used.

    Returns:
        bool: True if the authentication is successful, False otherwise.
    """
    if api_key_cvar.get() is not None:
        # Already authenticated
        return True
    
    organization = organization or organization_cvar.get()
    
    if api_key is None:
        # Try to get the api_key from the environment variable
        api_key = os.environ.get("HECTIQ_CONSOLE_API_KEY")

    if api_key is None:
        # Try to get the api_key from the credentials file
        import toml
        from pathlib import Path
        path = os.getenv("HECTIQ_CONSOLE_CREDENTIALS_FILE", 
                         os.path.join(Path.home(),".hectiq-console", "credentials.toml"))
        if not os.path.exists(path):
            return False
        with open(path, "r") as path:
            data = toml.load(path)

        if organization is not None:
            data = data.get(organization, {})
        else:
            # Multiple organizations
            if len(data)==0:
                return False
            
            organization = list(data.keys())[0]
            set_organization(organization) # Set the organization in the context
            data = list(data.values())[0]
      
        api_key = data.get("value")

        if api_key is None:
            return False

    api_key_cvar.set(api_key)
    return True

def get_authentification_headers() -> dict:
    """Get the authentification headers for the Hectiq Console. 
    Do not use this method directly. Instead, use the `authenticate` method.

    Returns:
        dict: Headers
    """
    is_logged = authenticate()
    if not is_logged:
        raise ValueError(f"You must authenticate to the Hectiq Console using the `hectiq_console.functional.authenticate` method or the command line `hectiq-console authenticate`. This error may occur if the organization ({get_organization()}) is not set or incorrect.")
    api_key = api_key_cvar.get()
    if api_key is None:
        raise ValueError("You must authenticate to the Hectiq Console using the `authenticate` method.")
    return {"X-API-Key": f"{api_key}"}

def create_incident(title: str, 
                    description: Optional[str] = None,
                    filenames: Optional[List] = None, 
                    resource: Optional[str] = None):
    """Create an incident in the Hectiq Console.

    Args:
        title (str): Title of the incident
        description (Optional[str], optional): Description of the incident. Defaults to None.
        resource (Optional[str], optional): Ressource ID of the resource to which the incident is related. 
            Defaults to None.
    """
    resource = get_resource(resource)
    body = {"name": title, "description": description}
    if filenames is not None:
        body["files"] = []
        for filename in filenames:
            assert os.path.exists(filename), f"File {filename} does not exist."
            name = os.path.basename(filename)
            num_bytes = os.path.getsize(filename)
            extension = os.path.splitext(filename)[1].replace(".", "")
            body["files"].append({"name": name, "num_bytes": num_bytes, "extension": extension})
    res = requests.post(f"{CONSOLE_APP_URL}/app/sender-client/{resource}/incidents", 
                 json=body)
    if res.status_code != 200:
        logger.error(f"⚠️ Error while creating the incident with hectiq_console.create_incident: {res.text}")
        return
    
    # Upload the files
    if filenames is not None:
        from hectiq_console.upload import upload_file
        for filename, policy in zip(filenames, res.json()["policies"]):
            upload_file(filepath=filename, policy=policy)

def add_file(filename: str,
             resource: Optional[str] = None):
    """Add a file to a resource in the Hectiq Console.

    Args:
        filename (str): Name of the file
        resource (Optional[str], optional): Ressource ID of the resource to which the file is related. 
            Defaults to None.
    """
    from hectiq_console.upload import upload_file
    resource = get_resource(resource)

    assert os.path.exists(filename), f"File {filename} does not exist."
    name = os.path.basename(filename)
    num_bytes = os.path.getsize(filename)
    extension = os.path.splitext(filename)[1].replace(".", "")
    json = {"name": name, "num_bytes": num_bytes, "extension": extension}
    res = requests.post(f"{CONSOLE_APP_URL}/app/sender-client/{resource}/files", json=json)
    if res.status_code != 200:
        logger.error(f"⚠️ Error while creating the file with hectiq_console.add_file: {res.text}")
        return
    try:
        policy = res.json()
    except:
        logger.error(f"⚠️ Error while creating the file with hectiq_console.add_file: {res.text}")
        return
    upload_file(filepath=filename, policy=policy)

def add_metrics(name: str, 
                value: Union[float, int], 
                resource: Optional[str] = None):
    """Add metrics to the Hectiq Console.

    Args:
        key (str): Key of the metrics
        value (Union[float, int]): Value of the metrics
        resource (Optional[str], optional): Ressource ID of the resource to which the metrics are related. 
            Defaults to None.
    """
    resource = get_resource(resource)
    body = {
        "metrics" : [{"name": name, "value": value}]
    }
    requests.post(f"{CONSOLE_APP_URL}/app/sender-client/{resource}/metrics", 
                 json=body)
    
def add_annotation(id: Optional[str] = None, 
                    inputs: Optional[Dict] = None,
                    outputs: Optional[Dict] = None,
                    metadata: Optional[Dict] = None,
                    resource: Optional[str] = None):
    """Add an annotation to the Hectiq Console. 
    For multiple annotations, you can use

    ```
    with hectiq_console.batch_annotations():
        hectiq_console.add_annotation(...)
        hectiq_console.add_annotation(...)
    ```
    Args:
        id (Optional[str], optional): ID of the annotation. Defaults to None.
        inputs (Optional[Dict], optional): Inputs of the annotation. Defaults to None.
        outputs (Optional[Dict], optional): Outputs of the annotation. Defaults to None.
        metadata (Optional[Dict], optional): Metadata of the annotation. Defaults to None.
        resource (Optional[str], optional): Ressource ID of the resource to which the annotation is related.
    """
    resource = get_resource(resource)
    data = {"inputs": inputs, "outputs": outputs, "metadata": metadata}
    if id is not None:
        data["id"] = id

    if batch_annotations_cvar.get() is not None:
        val = batch_annotations_cvar.get()
        val.append(data)
        batch_annotations_cvar.set(val)
        return
    
    res = requests.post(f"{CONSOLE_APP_URL}/app/sender-client/{resource}/annotations", 
                        json=data)
    if res.status_code != 200:
        logger.error(f"⚠️ Error while creating the annotation with hectiq_console.add_annotation: {res.text}")

def add_annotations(annotations: List[Dict],
                    resource: Optional[str] = None):
    """Add multiple annotations to the Hectiq Console.

    Args:
        annotations (List[Dict]): Annotations with optional keys `id`, `inputs`, `outputs` and `metadata`. 
        resource (Optional[str], optional): Ressource ID of the resource to which the annotations are related. 
            Defaults to None.
    """
    resource = get_resource(resource)
    data = {"annotations": annotations}
    res = requests.post(f"{CONSOLE_APP_URL}/app/sender-client/{resource}/batch-annotations",
                        json=data)
    if res.status_code != 200:
        logger.error(f"⚠️ Error while creating the annotations with hectiq_console.add_annotations: {res.text}")

def download_annotation(id: str,
                        resource: Optional[str] = None) -> dict:
    """Download an annotation from the Hectiq Console.

    Args:
        id (str): ID of the annotation
        resource (Optional[str], optional): Ressource ID of the resource to which the annotation is related. 
            Defaults to None.
    """
    resource = get_resource(resource)
    headers = get_authentification_headers()
    res = requests.get(f"{CONSOLE_APP_URL}/app/sender-client/{resource}/annotations/{id}", headers=headers)
    if res.status_code != 200:
        logger.error(f"⚠️ Error while downloading the annotation with hectiq_console.download_annotation: {res.text}")
        return
    return res.json()

def download_annotations(from_date: Optional[dt.datetime] = None,
                        to_date: Optional[dt.datetime] = None,
                        labels: Optional[List[str]] = None,
                        label_set: Literal["any", "all"] = "any",
                        fields: Optional[List[str]] = ["private_id", "inputs", "outputs", "metadata"],
                        page: Optional[int] = 1,
                        limit: Optional[int] = 100,
                        order_by: Optional[str] = None,
                        order_direction: Literal["asc", "desc"] = "asc",
                         resource: Optional[str] = None):
    """Download all annotations from the Hectiq Console.

    Args:
        resource (Optional[str], optional): Ressource ID of the resource to which the annotations are related. 
            Defaults to None.
    """
    resource = get_resource(resource)
    headers = get_authentification_headers()

    params = {
        "fields": fields,
        "created_from_date": from_date.toisoformat() if from_date is not None else None,
        "created_to_date": to_date.toisoformat() if to_date is not None else None,
        "labels": labels,
        "label_set": label_set,
        "page": page,
        "limit": limit,
        "order_by": order_by,
        "order_direction": order_direction
    }
    res = requests.get(f"{CONSOLE_APP_URL}/app/sender-client/{resource}/annotations", params=params, headers=headers)
    if res.status_code != 200:
        logger.error(f"⚠️ Error while downloading the annotations with hectiq_console.download_annotations: {res.text}")
        return
    return res.json()

def start_job(name: str, 
              description: Optional[str] = None, 
              metadata: Optional[Dict] = None,
              status: Optional[str] = None,
              resource: Optional[str] = None):
    """Start a job in the Hectiq Console.
    """

    if get_job() is not None:
        # Current job already started
        return
    
    resource = get_resource()
    body = {"name": name, 
            "description": description, 
            "metadata": metadata,
            "status": status}
    headers = get_authentification_headers()
    res = requests.post(f"{CONSOLE_APP_URL}/app/sender-client/{resource}/jobs", 
                 json=body, headers=headers)
    if res.status_code != 200:
        logger.error(f"⚠️ Error while starting the job with hectiq_console.start_job: {res.text}")
        return
    job_id = res.json().get("id")
    set_job(job_id)
    return True

def end_job(status: Optional[str] = None):
    """End the current job.
    """
    job_id = get_job()
    if job_id is None:
        # No job started
        return
    resource = get_resource()
    headers = get_authentification_headers()
    res = requests.post(f"{CONSOLE_APP_URL}/app/sender-client/{resource}/jobs/{job_id}/end", json={"status": status}, headers=headers)
    if res.status_code != 200:
        logger.error(f"⚠️ Error while ending the job with hectiq_console.end_job: {res.text}")
        return
    set_job(None)

def update_current_job(name: Optional[str] = None,
                          description: Optional[str] = None, 
                          metadata: Optional[Dict] = None,
                          status: Optional[str] = None):
    """Update the current job. 
    Only the non-null values are updated.
    """
    job_id = get_job()
    if job_id is None:
        # No job started
        return
    resource = get_resource()
    body = {"name": name, 
        "description": description, 
        "metadata": metadata,
        "status": status}
    # Remove null values
    body = {k: v for k, v in body.items() if v is not None}
    if len(body)==0:
        return
    headers = get_authentification_headers()
    res = requests.put(f"{CONSOLE_APP_URL}/app/sender-client/{resource}/jobs/{job_id}", 
                json=body, headers=headers)
    if res.status_code != 200:
        logger.error(f"⚠️ Error while updating the job with hectiq_console.update_current_job: {res.text}")
        return
    return True

def start_job_step(name: str, 
              description: Optional[str] = None, 
              metadata: Optional[Dict] = None,
              status: Optional[str] = None,
              resource: Optional[str] = None):
    """Start a job in the Hectiq Console.
    """
    job = get_job()
    if job is None:
        # No job started
        return
    
    if get_job_step() is not None:
        # Job step is started, close it
        end_job_step()
    
    resource = get_resource()
    body = {"name": name, 
            "description": description, 
            "metadata": metadata,
            "status": status}
    headers = get_authentification_headers()
    res = requests.post(f"{CONSOLE_APP_URL}/app/sender-client/{resource}/jobs/{job}/steps", 
                 json=body, headers=headers)
    if res.status_code != 200:
        logger.error(f"⚠️ Error while starting the job step with hectiq_console.start_job_step: {res.text}")
        return
    step_id = res.json().get("id")
    set_job_step(step_id)
    return True

def end_job_step(status: Optional[str] = None):
    """End the current job.
    """
    job_id = get_job()
    if job_id is None:
        # No job started
        return
    step_id = get_job_step()
    if step_id is None:
        # No job step started
        return
    resource = get_resource()
    headers = get_authentification_headers()
    res = requests.post(f"{CONSOLE_APP_URL}/app/sender-client/{resource}/job-steps/{step_id}/end", json={"status": status}, headers=headers)
    if res.status_code != 200:
        logger.error(f"⚠️ Error while ending the job step with hectiq_console.end_job_step: {res.text}")
        return
    set_job_step(None)

def update_current_job_step(name: Optional[str] = None,
                          description: Optional[str] = None, 
                          metadata: Optional[Dict] = None,
                          status: Optional[str] = None):
    """Update the current job. 
    Only the non-null values are updated.
    """
    job_id = get_job()
    if job_id is None:
        # No job started
        return
    step_id = get_job_step()
    if step_id is None:
        # No job step started
        return
    resource = get_resource()
    body = {"name": name, 
        "description": description, 
        "metadata": metadata,
        "status": status}
    # Remove null values
    body = {k: v for k, v in body.items() if v is not None}
    if len(body)==0:
        return
    headers = get_authentification_headers()
    res = requests.put(f"{CONSOLE_APP_URL}/app/sender-client/{resource}/job-steps/{step_id}", 
                json=body, headers=headers)
    if res.status_code != 200:
        logger.error(f"⚠️ Error while updating the job step with hectiq_console.update_current_job_step: {res.text}")
        return
    return True

class BatchDownloadAnnotations():
    """A helper class to download annotations. 

    Example:

    ```python
    for annotations in BatchDownloadAnnotations(batch=100):
        print(f"✅ Downloaded {len(annotations)} annotations.")
    ```
    """
    def __init__(self, batch: int = 100, **kwargs):
        self.kwargs = kwargs
        self.limit = batch
        self.page = 1

    def get(self):
        annotations = download_annotations(page=self.page, limit=self.limit, **self.kwargs)
        if annotations.get("total_pages") < self.page:
            raise StopIteration
        self.page += 1
        return annotations["results"]
    
    def __iter__(self):
        return self

    def __next__(self):
        return self.get()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.page = 1
        pass

@contextmanager
def timer_context(name: str, 
                  resource: Optional[str] = None):
    """Context manager to time a block of code.

    Args:
        key (str): Key of the timer
        resource (Optional[str], optional): Ressource ID of the resource to which the timer is related. 
            Defaults to None.
    """
    start = time.time()
    yield
    end = time.time()
    duration = end - start
    add_metrics(name=name, value=duration, resource=resource)

@contextmanager
def batch_annotations():
    """Context manager to batch the creation of annotations.
    """

    batch_annotations_cvar.set([])
    yield
    if len(batch_annotations_cvar.get())>0:
        add_annotations(annotations=batch_annotations_cvar.get())
    batch_annotations_cvar.set(None)

@contextmanager
def job_context(name: str, 
                      description: Optional[str] = None, 
                      metadata: Optional[Dict] = None,
                      status: Optional[str] = None,
                      resource: Optional[str] = None):
    """Context manager to start a job.

    Args:
        name (str): Name of the job
        description (Optional[str], optional): Description of the job. Defaults to None.
        metadata (Optional[Dict], optional): Metadata of the job. Defaults to None.
        status (Optional[str], optional): Status of the job. Defaults to None.
        resource (Optional[str], optional): Ressource ID of the resource to which the job is related. 
            Defaults to None.
    """
    start_job(name=name, 
              description=description, 
              metadata=metadata, 
              status=status,
              resource=resource)
    exception_raised = False
    try:
        yield
    except Exception as e:
        exception_raised = True
        raise e
    finally:
        # Catch all exceptions to end the job step
        if exception_raised:
            end_job_step(status="failed")
            end_job(status="failed")
        else:
            end_job_step()
            end_job()
            
@contextmanager
def job_step_context(name: str, 
                      description: Optional[str] = None, 
                      metadata: Optional[Dict] = None,
                      status: Optional[str] = None,
                      resource: Optional[str] = None):
    """Context manager to start a job step.

    Args:
        name (str): Name of the job step
        description (Optional[str], optional): Description of the job step. Defaults to None.
        metadata (Optional[Dict], optional): Metadata of the job step. Defaults to None.
        status (Optional[str], optional): Status of the job step. Defaults to None.
        resource (Optional[str], optional): Ressource ID of the resource to which the job step is related. 
            Defaults to None.
    """
    start_job_step(name=name, 
              description=description, 
              metadata=metadata, 
              status=status,
              resource=resource)
    exception_raised = False
    try:
        yield
    except Exception as e:
        exception_raised = True
        raise e
    finally:
        # Catch all exceptions to end the job step
        if exception_raised:
            end_job_step(status="failed")
        else:
            end_job_step()