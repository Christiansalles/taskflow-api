from enum import Enum
from typing import Optional
from pydantic import BaseModel, field_validator


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Status(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


# ---------------------------------------------------------------------------
# Title validation
# ---------------------------------------------------------------------------

def _validate_title(value: str) -> str:

    stripped = value.strip()
    if not stripped:
        raise ValueError("O título não pode ser vazio ou conter apenas espaços em branco")
    if len(stripped) > 100:
        raise ValueError("O título deve ter no máximo 100 caracteres")
    return stripped

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        return _validate_title(value)


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        return _validate_title(value)


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return _validate_title(value)


# ---------------------------------------------------------------------------
# Custom Exceptions
# ---------------------------------------------------------------------------

class TaskNotFoundException(Exception):
    def __init__(self, message: str = "Task not found") -> None:
        super().__init__(message)
        self.message = message


class InvalidStatusTransitionException(Exception):
    def __init__(self, message: str = "Invalid status transition") -> None:
        super().__init__(message)
        self.message = message
