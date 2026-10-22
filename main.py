from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="Task Manager API")

# ---------- Fake in-memory "database" (replaced by Postgres on Day 2-3) ----------
users_db: dict[int, dict] = {}
tasks_db: dict[int, dict] = {}
user_counter = 0
task_counter = 0


# ---------- Schemas (this is where validation happens) ----------
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    age: Optional[int] = Field(default=None, ge=13, le=120)


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    age: Optional[int]


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    priority: Priority = Priority.medium
    owner_id: int


class TaskOut(TaskCreate):
    id: int
    completed: bool = False
    created_at: datetime


# ---------- Endpoints ----------
@app.get("/")
def hello():
    return {"message": "Hello, FastAPI!"}


@app.get("/users", response_model=list[UserOut])
def list_users():
    return list(users_db.values())


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    user = users_db.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(task: TaskCreate):
    global task_counter
    # The owner must exist
    if task.owner_id not in users_db:
        raise HTTPException(status_code=404, detail="Owner not found")
    task_counter += 1
    record = {
        "id": task_counter,
        **task.model_dump(),
        "completed": False,
        "created_at": datetime.utcnow(),
    }
    tasks_db[task_counter] = record
    return record


@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(owner_id: Optional[int] = None):
    tasks = list(tasks_db.values())
    if owner_id is not None:
        tasks = [t for t in tasks if t["owner_id"] == owner_id]
    return tasks