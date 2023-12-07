from typing import Any, Dict

from seaplane.config import config
from seaplane.logs import log

from .decorators import Context
from .executor import RealTaskExecutor, SchemaExecutor


def build_schema(context: Context) -> Dict[str, Any]:
    """
    Constructs a JSON-friendly / simple type structure describing
    the project by running the application SchemaExecutors and analysing
    the resulting structure of apps and tasks.
    """
    schema: Dict[str, Any] = {"apps": {}}

    # Gathers task.sources together and otherwise does evil magic
    # to assemble the Task / App structure.
    context.set_executor(SchemaExecutor())

    apps_and_returns = [(app, app.func("entry_point")) for app in context.apps]

    context.set_executor(RealTaskExecutor())

    for app, returns in apps_and_returns:
        app_desc: Dict[str, Any] = {
            "id": app.id,
            "entry_point": {"type": app.type, "parameters": app.parameters},
            "tasks": [],
            "io": {},
        }

        for task in app.tasks:
            task_desc = {
                "id": task.id,
                "name": task.name,
                "replicas": task.replicas,
                "ack_wait": task.ack_wait,
            }

            for source in task.sources:
                if not app_desc["io"].get(source, None):
                    app_desc["io"][source] = [task.id]
                else:
                    app_desc["io"][source].append(task.id)

            app_desc["tasks"].append(task_desc)

        app_desc["io"]["returns"] = returns
        schema["apps"][app.id] = app_desc

    schema["carrier_endpoint"] = config.carrier_endpoint
    schema["identity_endpoint"] = config.identify_endpoint

    log.info("Apps build successfully!\n")

    return schema
