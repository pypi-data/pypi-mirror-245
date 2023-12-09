import hashlib
import json
import os
import shutil
import toml
from typing import cast, Any, Dict, List, Optional
from urllib.parse import urlparse
import zipfile

import requests
import time

from seaplane.config import Configuration, config, runner_image
from seaplane.errors import SeaplaneError
from seaplane.logs import log
from seaplane.object import ObjectStorageAPI, object_store
from seaplane.sdk_internal_utils.http import headers
from seaplane.sdk_internal_utils.token_auth import with_token
from seaplane_framework.api.exceptions import ApiException

from .app import App
from .debug_schema import build_debug_schema
from .decorators import context
from .task import Task
from .executor import SchemaExecutor

PROJECT_TOML = "pyproject.toml"
ENDPOINTS_STREAM = "_SEAPLANE_ENDPOINT"

SecretKey = str
SecretValue = str


def endpoints_input_subject(app_id: str) -> str:
    """
    The default stream name for the application as a whole. Requests to the
    app endpoint will end up on this stream.
    """
    return f"{ENDPOINTS_STREAM}.in.{app_id}.*"


def _file_md5(path: str) -> str:
    """
    Gets the MD5 hash of a file by path.
    """

    hasher = hashlib.md5()
    block_size = 4194304  # 4 MB
    with open(path, "rb") as fh:
        while True:
            buffer = fh.read(block_size)
            if not buffer:
                break
            hasher.update(buffer)
    return hasher.hexdigest()


def endpoints_output_subject(app_id: str) -> str:
    """
    The default output stream for the app as a whole, and for this
    request id in particular.
    """
    # The following ${! ... } incantations are Benthos function interpolation
    request_id = '${! meta("_seaplane_request_id") }'
    joined_batch_hierarchy = '${! meta("_seaplane_batch_hierarchy") }'
    return f"{ENDPOINTS_STREAM}.out.{app_id}.{request_id}{joined_batch_hierarchy}"


def task_subject(app_id: str, task_id: str) -> str:
    return f"{app_id}.{task_id}"


def create_bucket_if_needed(app_id: str, bucket_name: str) -> str:
    """
    Returns the notification stream associated with a given bucket,
    after either creating the bucket with a default notification subject name,
    or reading the notification subject name from an existing bucket.

    Will throw an exception if the bucket cannot be created, or if the
    bucket already exists but is not configured to send notifications.
    """
    try:
        bkt = object_store.get_bucket(bucket_name)
        if "notify" not in bkt:
            raise SeaplaneError(
                f"bucket {bucket_name} already exists, but is not configured for notifications."
                " The seaplane project can create a new correctly configured bucket for you,"
                " but if you want to create one yourself, make sure it has an associated"
                " notify subject for your task to listen to."
            )
        ret = cast(str, bkt["notify"])
        log.debug(f"using existing bucket {bucket_name} with subject {ret}")
        return ret
    except ApiException as e:
        if e.status != 404:
            raise

    log.info(f"creating bucket {bucket_name} with default attributes")
    notify = f"{bucket_name}-evts.updates"
    bucket_def = {
        "description": f"Automatically created for application {app_id}",
        "replicas": 3,
        "max_bytes": -1,
        "notify": notify,
    }
    object_store.create_bucket(bucket_name, bucket_def)

    return notify


def build_task_flow_config(
    app: App,
    task: Task,
    project_url: str,
    bucket_subjects: Dict[str, str],  # mapping of bucket name to notification stream name
) -> Dict[str, Any]:
    if task.uses_endpoint() and app.type == "stream":  # User override
        input = app.parameters[0]
    elif task.watch_bucket is not None:  # Bind to watch bucket
        input = bucket_subjects[task.watch_bucket]
    elif task.uses_endpoint():  # read from the endpoint default stream
        input = endpoints_input_subject(app.id)
    else:  # listen to interior wire-ups
        input = task_subject(app.id, task.id)

    output: Optional[Dict[str, Any]] = None

    next_subjects = [
        task_subject(app.id, peer.id) for peer in app.tasks if task.id in peer.sources
    ]
    if app.returns == task.id:
        next_subjects.append(endpoints_output_subject(app.id))

    if len(next_subjects) > 1:
        output = {
            "broker": {"outputs": [{"carrier": {"subject": subject}} for subject in next_subjects]}
        }
    elif len(next_subjects) == 1:
        output = {
            "carrier": {"subject": next_subjects[0]},
        }

    ack_wait = f"{str(task.ack_wait)}m"

    workload = {
        "input": {
            "carrier": {
                "stream": input.split(".", 1)[0],
                "subject": input,
                "durable": task.id,
                "ack_wait": ack_wait,
                "bind": True,
            },
        },
        "processor": {
            "docker": {
                "image": runner_image(),
                "args": [project_url],
            }
        },
        "output": output,
        "replicas": task.replicas,
    }

    log.debug(f"Created {task.id} workload")
    log.debug(json.dumps(workload, indent=2))

    return workload


@with_token
def create_stream(token: str, name: str) -> None:
    log.debug(f"Creating stream: {name}")
    url = f"{config.carrier_endpoint}/stream/{name}"

    payload: Dict[str, Any] = {"ack_timeout": 20}  # should be long enough for OpenAI
    if config.region is not None:
        payload["allow_locations"] = [f"region/{config.region}"]
    resp = requests.put(
        url,
        json=payload,
        headers=headers(token),
    )
    resp.raise_for_status()


@with_token
def delete_stream(token: str, name: str) -> None:
    log.debug(f"deleting stream: {name}")
    url = f"{config.carrier_endpoint}/stream/{name}"

    resp = requests.delete(
        url,
        headers=headers(token),
    )
    resp.raise_for_status()


def get_secrets(config: Configuration) -> Dict[SecretKey, SecretValue]:
    secrets = {}
    for key, value in config._api_keys.items():
        secrets[key] = value

    return secrets


@with_token
def add_secrets(token: str, name: str, secrets: Dict[SecretKey, SecretValue]) -> None:
    log.debug(f"adding secrets: {name}")
    url = f"{config.carrier_endpoint}/flow/{name}/secrets"
    if config.dc_region is not None:
        url += f"?region={config.dc_region}"

    flow_secrets = {}
    for secret_key, secret_value in secrets.items():
        flow_secrets[secret_key] = {"destination": "all", "value": secret_value}

    resp = requests.put(
        url,
        json=flow_secrets,
        headers=headers(token),
    )
    resp.raise_for_status()


@with_token
def create_flow(token: str, name: str, workload: Dict[str, Any]) -> None:
    log.debug(f"creating flow: {name}")
    url = f"{config.carrier_endpoint}/flow/{name}"
    if config.dc_region is not None:
        url += f"?region={config.dc_region}"

    resp = requests.put(
        url,
        json=workload,
        headers=headers(token),
    )
    resp.raise_for_status()


@with_token
def delete_flow(token: str, name: str) -> None:
    log.debug(f"deleting flow: {name}")

    url = f"{config.carrier_endpoint}/flow/{name}"
    if config.dc_region is not None:
        url += f"?region={config.dc_region}"

    resp = requests.delete(
        url,
        headers=headers(token),
    )
    resp.raise_for_status()


def zip_current_directory(tenant: str, project_name: str) -> str:
    current_directory = os.getcwd()
    zip_filename = f"./build/{tenant}.zip"

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(PROJECT_TOML, os.path.relpath(PROJECT_TOML, current_directory))

        env_file = os.environ.get("SEAPLANE_ENV_FILE", ".env")
        if os.path.exists(env_file):
            zipf.write(env_file, os.path.relpath(".env", current_directory))

        for root, _, files in os.walk(f"{current_directory}/{project_name}"):
            for file in files:
                if "__pycache__" in root:
                    continue

                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, current_directory))

    return zip_filename


def upload_project(project: Dict[str, Any], tenant: str) -> str:
    """
    Zips the project directory and pushes it into the Seaplane object store,
    returning a URL that our executor image can use to refer back to the
    project when executing.
    """

    # Step 1: Make sure we have a bucket to dump our project into
    default_bucket_name: str = "seaplane-internal-flows"
    default_bucket_config = {
        "description": "Seaplane bucket used for flow images. Should not be modified directly.",
        "replicas": 3,
        "max_bytes": -1,  # unlimited
        "allow_locations": ["all"],  # TODO: Georestrictions
    }

    obj = ObjectStorageAPI()
    obj._allow_internal = True
    if default_bucket_name not in obj.list_buckets():
        obj.create_bucket(default_bucket_name, default_bucket_config)

    # Step 2: Build the zip file
    project_name: str = project["tool"]["poetry"]["name"]
    project_file = zip_current_directory(tenant, project_name)
    remote_path = project_name + "." + _file_md5(project_file) + ".zip"

    # Step 3: Upload & return
    #  Retry upload if there is an exception (e.g., 500 timeout)
    for i in range(1, 4):
        try:
            obj.upload_file(default_bucket_name, remote_path, project_file)
            break
        except ApiException:
            time.sleep(i * 2)
            log.info(" retrying upload")

    obj_url = obj.file_url(default_bucket_name, remote_path)
    log.info(f"uploaded project package {obj_url}")

    return obj_url


def print_endpoints(apps: List[App]) -> None:
    endpoint_apps = [a for a in apps if any(task.uses_endpoint() for task in a.tasks)]
    if len(endpoint_apps) > 0:
        log.info("\nDeployed Endpoints:\n")

    for app in endpoint_apps:
        if app.type == "API":
            log.info(
                f"{app.id} Endpoint: POST "
                f"https://{urlparse(config.carrier_endpoint).netloc}/v1/endpoints/{app.id}/request"
            )
            log.info(
                f"{app.id} CLI Command: plane endpoints request {app.id} -d <data> OR @<file>"
            )
        elif app.type == "stream" and len(app.parameters) >= 1:
            log.info(f"🚀 {app.id} using stream subject {app.parameters[0]} as entry point")

    if len(endpoint_apps) > 0:
        print("\n")


def deploy_task(
    app: App,
    task: Task,
    secrets: Dict[SecretKey, SecretValue],
    bucket_subjects: Dict[str, str],  # mapping of bucket names to their associated notify subjects
    project_url: str,
) -> None:
    delete_flow(task.id)

    workload = build_task_flow_config(app, task, project_url, bucket_subjects)

    create_flow(task.id, workload)
    secrets = secrets.copy()
    secrets["TASK_ID"] = task.id
    secrets["SAVE_RESULT_TASK"] = json.dumps(app.returns == task.id)
    add_secrets(task.id, secrets)

    # Log some useful info about where this is deployed
    #  Note that region info is only included if we have set it
    deploy_info = ""
    if "staging" in config.carrier_endpoint:
        deploy_info += " in staging"
    if config.dc_region is not None:
        deploy_info += f" in {config.dc_region} data center"
    log.info(f"Deploy for task {task.id} done{deploy_info}")


def run_deploy() -> None:
    """
    Top level task for deploying an application, called from the CLI.
    Writes files, posts and destroys new Seaplane resources, writes logs.
    """
    secrets = get_secrets(config)
    if not config._token_api.api_key:
        log.info("API KEY not set. Please set in .env or seaplane.config.set_api_key()")
        return

    shutil.rmtree("build/", ignore_errors=True)

    # Spider the apps and tasks finalize their structure.
    context.set_executor(SchemaExecutor())
    for app in context.apps:
        app.assemble()

    # Create buckets and get associated notify subjects if necessary.
    bucket_subjects = {}
    for app in context.apps:
        for task in app.tasks:
            if task.watch_bucket:
                bucket_subjects[task.watch_bucket] = create_bucket_if_needed(
                    app.id, task.watch_bucket
                )

    # Write out schema for use with other tooling
    debug_schema = build_debug_schema(context.apps)

    if not os.path.exists("build"):
        os.makedirs("build")

    with open(os.path.join("build", "schema.json"), "w") as file:
        json.dump(debug_schema, file, indent=2)

    # use the apps and tasks directly for the rest of the deployment
    debug_schema = None  # type: ignore

    # Upload project assets
    tenant = config._token_api.get_tenant()
    pyproject = toml.loads(open(PROJECT_TOML, "r").read())
    project_url = upload_project(pyproject, tenant)

    deploy_info = ""
    if "staging" in config.carrier_endpoint:
        deploy_info += " in staging"
    if config.region is not None:
        deploy_info += f" in {config.region} region"

    log.info(f"Deploying everything{deploy_info}...")

    bucket_streams = {v.split(".", 1)[0] for v in bucket_subjects.values()}
    for stream in bucket_streams:
        delete_stream(stream)
        create_stream(stream)

    for app in context.apps:
        delete_stream(app.id)
        create_stream(app.id)

        for task in app.tasks:
            deploy_task(app, task, secrets, bucket_subjects, project_url)

    print_endpoints(context.apps)

    log.info("🚀 Deployment complete")


def destroy() -> None:
    """
    Top level call to delete Seaplane resources associated with this project.
    """
    if not config._token_api.api_key:
        log.info("API KEY not set. Please set in .env or seaplane.config.set_api_key()")
        return

    # Consider loading the existing schema like status when you destroy
    context.set_executor(SchemaExecutor())
    for app in context.apps:
        app.assemble()

    for app in context.apps:
        delete_stream(app.id)

        for task in app.tasks:
            delete_flow(task.id)
