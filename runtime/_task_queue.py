from queue import Queue
from typing import Any
_task_queue = Queue()

def put_task(task: Any) -> None:
    _task_queue.put(task)

def get_task() -> Any:
    return _task_queue.get()
