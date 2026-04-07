from .models import Status, Task, TaskCreate, TaskUpdate, TaskNotFoundException, InvalidStatusTransitionException
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

    def get_task(self, task_id: int) -> Task:
        """Return the task by ID, or raise TaskNotFoundException if it doesn't exist."""
        task = self._repository.find_by_id(task_id)
        if not task:
            raise TaskNotFoundException()
        return task

    def update_task(self, task_id: int, data: TaskUpdate) -> Task:
        """Update an existing task with the provided fields."""
        task = self.get_task(task_id)
        
        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        if data.priority is not None:
            task.priority = data.priority
        if data.status is not None:
            task.status = data.status
            
        return self._repository.update(task)

    def delete_task(self, task_id: int) -> bool:
        """Delete an existing task by ID."""
        self.get_task(task_id)
        self._repository.delete(task_id)
        return True

    def complete_task(self, task_id: int) -> Task:
        """Mark a task as completed.
        
        Raises:
            InvalidStatusTransitionException: If the task is already DONE.
        """
        task = self.get_task(task_id)
        if task.status == Status.DONE:
            raise InvalidStatusTransitionException()
        
        task.status = Status.DONE
        return self._repository.update(task)
