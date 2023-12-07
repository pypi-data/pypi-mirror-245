import secrets
import string
from typing import Any, Callable, List

from ..logs import log
from .task import Task


def random_id() -> str:
    alphabet = string.ascii_letters + string.digits
    random_string = "".join(secrets.choice(alphabet) for i in range(10))
    return random_string


class App:
    def __init__(
        self,
        func: Callable[[Any], Any],
        type: str,  # "stream" or "API"
        parameters: List[str],  # when type == "stream", [STREAM_NAME]
        id: str,
    ) -> None:
        self.id = id
        self.func = func
        self.type = type
        self.parameters = parameters
        self.tasks: List[Task] = []
        self.return_source = None

    def process(self, *args: Any, **kwargs: Any) -> Any:
        self.func(*args, *kwargs)

    def add_task(self, task: Task) -> None:
        for i, cp in enumerate(self.tasks):
            if cp.id == task.id:
                self.tasks[i] = task
                return
        self.tasks.append(task)

    def print(self) -> None:
        log.info(f"id: {self.id}, type: {self.type}, parameters: {self.parameters}")
