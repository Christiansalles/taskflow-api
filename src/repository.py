from .models import Task


class TaskRepository:
    """In-memory repository for Task persistence."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def generate_id(self) -> int:
        """Return the next available ID and increment the counter."""
        task_id = self._next_id
        self._next_id += 1
        return task_id

    def save(self, task: Task) -> Task:
        """Persist a new task and return it."""
        self._tasks[task.id] = task
        return task

    def find_by_id(self, task_id: int) -> Task | None:
        """Return the task with the given ID, or None if not found."""
        return self._tasks.get(task_id)

    def find_all(self) -> list[Task]:
        """Return all stored tasks."""
        return list(self._tasks.values())

    def update(self, task: Task) -> Task:
        """Replace an existing task with the updated version and return it."""
        self._tasks[task.id] = task
        return task

    def delete(self, task_id: int) -> bool:
        """Remove a task by ID. Returns True if it existed, False otherwise."""
        if task_id in self._tasks:
            del self._tasks[task_id]  
            return True
        return False
