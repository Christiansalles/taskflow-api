import pytest
from src.models import Priority, Status, TaskUpdate


class TestGetTask:
    """Testes para TaskService.get_task()"""

    def test_get_task_returns_task_when_found(self, task_service, mock_repository, sample_task):
        pass

    def test_get_task_raises_when_not_found(self, task_service, mock_repository):
        pass


class TestListTasks:
    """Testes para TaskService.list_tasks()"""

    def test_list_tasks_returns_all(self, task_service, mock_repository, sample_task):
        pass

    def test_list_tasks_returns_empty_list(self, task_service, mock_repository):
        pass


class TestCreateTask:
    """Testes para TaskService.create_task()"""

    def test_create_task_returns_created_task(
        self, task_service, mock_repository, sample_task_create, sample_task
    ):
        pass

    def test_create_task_calls_repository_save(
        self, task_service, mock_repository, sample_task_create
    ):
        pass


class TestUpdateTask:
    """Testes para TaskService.update_task()"""

    def test_update_task_changes_fields(self, task_service, mock_repository, sample_task):
        pass

    def test_update_task_raises_when_not_found(self, task_service, mock_repository):
        pass


class TestDeleteTask:
    """Testes para TaskService.delete_task()"""

    def test_delete_task_returns_true_when_deleted(self, task_service, mock_repository):
        pass

    def test_delete_task_raises_when_not_found(self, task_service, mock_repository):
        pass
