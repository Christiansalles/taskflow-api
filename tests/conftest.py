import pytest
from unittest.mock import MagicMock

from src.repository import TaskRepository
from src.service import TaskService
from src.models import Task, TaskCreate, Priority, Status


@pytest.fixture
def mock_repository():
    """Mock do TaskRepository — substitui o repositório real nos testes."""
    return MagicMock(spec=TaskRepository)


@pytest.fixture
def task_service(mock_repository):
    """TaskService com repositório mockado injetado."""
    return TaskService(repository=mock_repository)


@pytest.fixture
def sample_task():
    """Tarefa válida para reuso nos testes."""
    return Task(
        id=1,
        title="Tarefa de exemplo",
        description="Descrição da tarefa",
        priority=Priority.MEDIUM,
        status=Status.PENDING,
    )


@pytest.fixture
def sample_task_create():
    """Payload de criação válido para reuso nos testes."""
    return TaskCreate(
        title="Nova tarefa",
        description="Descrição",
        priority=Priority.LOW,
    )
