from .models import Status, Task, TaskCreate
from .repository import TaskRepository


class TaskService:
    """Business logic layer for task management."""

    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    def create_task(self, data: TaskCreate) -> Task:

        task = Task(
            id=self._repository.generate_id(),
            title=data.title,
            description=data.description,
            priority=data.priority,
            status=Status.PENDING,
        )
        return self._repository.save(task)

    def list_tasks(self) -> list[Task]:
        """Return all stored tasks."""
        return self._repository.find_all()

    def list_by_status(self, status: Status) -> list[Task]:
        """Return all tasks filtered by status."""
        return self._repository.find_by_status(status)
