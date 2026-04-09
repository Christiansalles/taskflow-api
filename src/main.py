from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from .models import (
    InvalidStatusTransitionException,
    Task,
    TaskCreate,
    TaskNotFoundException,
    TaskUpdate,
)
from .repository import TaskRepository
from .service import TaskService


app = FastAPI(
    title="TaskFlow API",
    description="REST API para gerenciamento de tarefas com pipeline CI/CD",
    version="1.0.0",
)

# Singletons (Injeção de Dependências Manual)
repository = TaskRepository()
service = TaskService(repository)


# ---------------------------------------------------------------------------
# Exception Handlers
# ---------------------------------------------------------------------------

@app.exception_handler(TaskNotFoundException)
async def task_not_found_handler(request: Request, exc: TaskNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


@app.exception_handler(InvalidStatusTransitionException)
async def invalid_status_transition_handler(request: Request, exc: InvalidStatusTransitionException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.message},
    )


# ---------------------------------------------------------------------------
# Endpoints CRUD
# ---------------------------------------------------------------------------

@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=Task)
def create_task(data: TaskCreate):
    try:
        return service.create_task(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return service.list_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    return service.get_task(task_id)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskUpdate):
    return service.update_task(task_id, data)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    service.delete_task(task_id)


@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int):
    return service.complete_task(task_id)