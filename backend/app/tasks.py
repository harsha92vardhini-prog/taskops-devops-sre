from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Task

router = APIRouter(prefix="/tasks", tags=["Tasks"])


class TaskCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)


@router.post("", status_code=201)
def create_task(payload: TaskCreate) -> dict:
    with Session(engine) as session:
        task = Task(
            title=payload.title,
            description=payload.description,
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
        }


@router.get("")
def list_tasks() -> list[dict]:
    from sqlalchemy import select

    with Session(engine) as session:
        tasks = session.scalars(
            select(Task).order_by(Task.id).limit(100)
        ).all()

        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
            }
            for task in tasks
        ]


from typing import Literal
from fastapi import HTTPException


class TaskStatusUpdate(BaseModel):
    status: Literal["todo", "in_progress", "done"]


@router.patch("/{task_id}")
def update_task_status(task_id: int, payload: TaskStatusUpdate) -> dict:
    with Session(engine) as session:
        task = session.get(Task, task_id)

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        task.status = payload.status
        session.commit()
        session.refresh(task)

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
        }


from fastapi import Response


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int) -> Response:
    with Session(engine) as session:
        task = session.get(Task, task_id)

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        session.delete(task)
        session.commit()

        return Response(status_code=204)


from fastapi import Response


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int) -> Response:
    with Session(engine) as session:
        task = session.get(Task, task_id)

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        session.delete(task)
        session.commit()

        return Response(status_code=204)
