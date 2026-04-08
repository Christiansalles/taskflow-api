"""
20 cenários de teste unitário para TaskService.

Organização por classe:
  TestCreateTask    — cenários 1, 7, 10
  TestListTasks     — cenários 2, 8
  TestGetTask       — cenário  3
  TestUpdateTask    — cenários 4, 9
  TestDeleteTask    — cenário  5
  TestCompleteTask  — cenário  6
  TestEdgeCases     — cenários 11-20
"""

import pytest
from pydantic import ValidationError
from unittest.mock import MagicMock

from src.models import (
    Priority,
    Status,
    Task,
    TaskCreate,
    TaskUpdate,
    TaskNotFoundException,
    InvalidStatusTransitionException,
)


# ===========================================================================
# 1-3  TestCreateTask — fluxo de criação
# ===========================================================================

class TestCreateTask:
    """Testes de criação de tarefas — cenários de caminho feliz."""

    def test_create_task_with_valid_data(self, task_service, mock_repository):
        """Cenário 1 — mock de save e generate_id, verifica Task com status PENDING."""
        mock_repository.generate_id.return_value = 42
        mock_repository.save.return_value = Task(
            id=42,
            title="Nova tarefa",
            description="Descrição",
            priority=Priority.MEDIUM,
            status=Status.PENDING,
        )

        data = TaskCreate(title="Nova tarefa", description="Descrição", priority=Priority.MEDIUM)
        result = task_service.create_task(data)

        mock_repository.generate_id.assert_called_once()
        mock_repository.save.assert_called_once()
        assert result.status == Status.PENDING
        assert result.title == "Nova tarefa"

    def test_create_task_with_high_priority(self, task_service, mock_repository):
        """Cenário 7 — verifica que Priority.HIGH é preservada na criação."""
        mock_repository.generate_id.return_value = 2
        mock_repository.save.return_value = Task(
            id=2,
            title="Tarefa urgente",
            priority=Priority.HIGH,
            status=Status.PENDING,
        )

        data = TaskCreate(title="Tarefa urgente", priority=Priority.HIGH)
        result = task_service.create_task(data)

        assert result.priority == Priority.HIGH
        assert result.status == Status.PENDING

    def test_create_multiple_tasks(self, task_service, mock_repository):
        """Cenário 10 — chama create_task duas vezes, verifica que save foi chamado duas vezes."""
        mock_repository.generate_id.side_effect = [1, 2]
        mock_repository.save.side_effect = [
            Task(id=1, title="Tarefa A", status=Status.PENDING, priority=Priority.MEDIUM),
            Task(id=2, title="Tarefa B", status=Status.PENDING, priority=Priority.LOW),
        ]

        task_service.create_task(TaskCreate(title="Tarefa A"))
        task_service.create_task(TaskCreate(title="Tarefa B", priority=Priority.LOW))

        assert mock_repository.save.call_count == 2


# ===========================================================================
# 4-5  TestListTasks — fluxo de listagem
# ===========================================================================

class TestListTasks:
    """Testes de listagem de tarefas — cenários de caminho feliz."""

    def test_list_tasks_returns_all(self, task_service, mock_repository, sample_task):
        """Cenário 2 — mock de find_all retornando lista com 2 tarefas, verifica tamanho."""
        segunda_tarefa = Task(
            id=2, title="Segunda tarefa", priority=Priority.HIGH, status=Status.PENDING
        )
        mock_repository.find_all.return_value = [sample_task, segunda_tarefa]

        result = task_service.list_tasks()

        mock_repository.find_all.assert_called_once()
        assert len(result) == 2

    def test_list_tasks_by_pending_status(self, task_service, mock_repository, sample_task):
        """Cenário 8 — mock de find_by_status, verifica filtragem por PENDING."""
        mock_repository.find_by_status.return_value = [sample_task]

        result = task_service.list_by_status(Status.PENDING)

        mock_repository.find_by_status.assert_called_once_with(Status.PENDING)
        assert len(result) == 1
        assert result[0].status == Status.PENDING


# ===========================================================================
# 6-7  TestGetTask — fluxo de busca por ID
# ===========================================================================

class TestGetTask:
    """Testes de busca de tarefa por ID."""

    def test_get_task_by_existing_id(self, task_service, mock_repository, sample_task):
        """Cenário 3 — mock de find_by_id retornando tarefa, verifica retorno correto."""
        mock_repository.find_by_id.return_value = sample_task

        result = task_service.get_task(1)

        mock_repository.find_by_id.assert_called_once_with(1)
        assert result.id == sample_task.id
        assert result.title == sample_task.title


# ===========================================================================
# 8-9  TestUpdateTask — fluxo de atualização
# ===========================================================================

class TestUpdateTask:
    """Testes de atualização de tarefas — cenários de caminho feliz."""

    def test_update_task_title(self, task_service, mock_repository, sample_task):
        """Cenário 4 — mock de find_by_id e update, verifica que título foi atualizado."""
        mock_repository.find_by_id.return_value = sample_task
        updated = Task(
            id=sample_task.id,
            title="Título atualizado",
            description=sample_task.description,
            priority=sample_task.priority,
            status=sample_task.status,
        )
        mock_repository.update.return_value = updated

        result = task_service.update_task(1, TaskUpdate(title="Título atualizado"))

        mock_repository.update.assert_called_once()
        assert result.title == "Título atualizado"

    def test_update_description_keeps_status(self, task_service, mock_repository, sample_task):
        """Cenário 9 — atualiza só descrição, verifica que status não muda."""
        original_status = sample_task.status
        mock_repository.find_by_id.return_value = sample_task
        mock_repository.update.return_value = Task(
            id=sample_task.id,
            title=sample_task.title,
            description="Nova descrição",
            priority=sample_task.priority,
            status=original_status,
        )

        result = task_service.update_task(1, TaskUpdate(description="Nova descrição"))

        assert result.status == original_status
        assert result.description == "Nova descrição"


# ===========================================================================
# 10  TestDeleteTask — fluxo de exclusão
# ===========================================================================

class TestDeleteTask:
    """Testes de exclusão de tarefa."""

    def test_delete_existing_task(self, task_service, mock_repository, sample_task):
        """Cenário 5 — mock de find_by_id e delete, verifica retorno True."""
        mock_repository.find_by_id.return_value = sample_task
        mock_repository.delete.return_value = True

        result = task_service.delete_task(1)

        mock_repository.find_by_id.assert_called_once_with(1)
        mock_repository.delete.assert_called_once_with(1)
        assert result is True


# ===========================================================================
# 11  TestCompleteTask — fluxo de conclusão
# ===========================================================================

class TestCompleteTask:
    """Testes de conclusão de tarefa."""

    def test_complete_pending_task(self, task_service, mock_repository, sample_task):
        """Cenário 6 — mock de find_by_id e update, verifica que status vai para DONE."""
        mock_repository.find_by_id.return_value = sample_task
        completed = Task(
            id=sample_task.id,
            title=sample_task.title,
            description=sample_task.description,
            priority=sample_task.priority,
            status=Status.DONE,
        )
        mock_repository.update.return_value = completed

        result = task_service.complete_task(1)

        mock_repository.update.assert_called_once()
        assert result.status == Status.DONE


# ===========================================================================
# 12-20  TestEdgeCases — casos extremos e de erro
# ===========================================================================

class TestEdgeCases:
    """Testes de casos extremos e tratamento de erro — cenários 11-20."""

    def test_get_task_not_found_raises_exception(self, task_service, mock_repository):
        """Cenário 11 — mock de find_by_id retornando None, verifica TaskNotFoundException."""
        mock_repository.find_by_id.return_value = None

        with pytest.raises(TaskNotFoundException):
            task_service.get_task(999)

    def test_create_task_empty_title_raises_error(self, task_service):
        """Cenário 12 — title='' deve lançar ValueError via Pydantic."""
        with pytest.raises(ValueError):
            TaskCreate(title="")

    def test_create_task_whitespace_title_raises_error(self, task_service):
        """Cenário 13 — title='   ' deve lançar ValueError via Pydantic."""
        with pytest.raises(ValueError):
            TaskCreate(title="   ")

    def test_delete_nonexistent_task_raises_exception(self, task_service, mock_repository):
        """Cenário 14 — mock de find_by_id retornando None, verifica TaskNotFoundException."""
        mock_repository.find_by_id.return_value = None

        with pytest.raises(TaskNotFoundException):
            task_service.delete_task(999)

    def test_update_nonexistent_task_raises_exception(self, task_service, mock_repository):
        """Cenário 15 — mock de find_by_id retornando None, verifica TaskNotFoundException."""
        mock_repository.find_by_id.return_value = None

        with pytest.raises(TaskNotFoundException):
            task_service.update_task(999, TaskUpdate(title="Qualquer"))

    def test_complete_already_done_task_raises_exception(
        self, task_service, mock_repository, sample_task
    ):
        """Cenário 16 — tarefa com status DONE, verifica InvalidStatusTransitionException."""
        done_task = Task(
            id=sample_task.id,
            title=sample_task.title,
            description=sample_task.description,
            priority=sample_task.priority,
            status=Status.DONE,
        )
        mock_repository.find_by_id.return_value = done_task

        with pytest.raises(InvalidStatusTransitionException):
            task_service.complete_task(done_task.id)

    def test_create_task_title_too_long_raises_error(self, task_service):
        """Cenário 17 — title com 101 caracteres deve lançar ValueError via Pydantic."""
        title_101 = "a" * 101

        with pytest.raises(ValueError):
            TaskCreate(title=title_101)

    def test_create_task_invalid_priority(self, task_service):
        """Cenário 18 — priority com valor inválido deve lançar ValidationError do Pydantic."""
        with pytest.raises(ValidationError):
            TaskCreate(title="Tarefa válida", priority="INVALIDO")  # type: ignore[arg-type]

    def test_list_tasks_when_repository_raises_exception(self, task_service, mock_repository):
        """Cenário 19 — mock de find_all lançando Exception, verifica propagação."""
        mock_repository.find_all.side_effect = Exception("Erro de banco")

        with pytest.raises(Exception, match="Erro de banco"):
            task_service.list_tasks()

    def test_update_task_with_no_fields_keeps_original(
        self, task_service, mock_repository, sample_task
    ):
        """Cenário 20 — TaskUpdate com todos campos None, verifica que tarefa não muda."""
        mock_repository.find_by_id.return_value = sample_task
        mock_repository.update.return_value = sample_task  # repositório devolve a mesma

        result = task_service.update_task(sample_task.id, TaskUpdate())

        assert result.title == sample_task.title
        assert result.description == sample_task.description
        assert result.priority == sample_task.priority
        assert result.status == sample_task.status
