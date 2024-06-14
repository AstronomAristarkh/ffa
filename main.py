from fastapi import FastAPI, HTTPException
import logging
from pydantic import BaseModel
from typing import Optional


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Optional[bool] = False

tasks = []

@app.get("/task/", response_model=list[Task])
async def get_tasks():
    return [task for task in tasks if not task.status]

@app.get("/task/{id}", response_model=Task)
async def get_task():
    task = [task for task in tasks if task.id==id]
    if not task:
        raise HTTPException(status_code=404, detail="Task did not found")
    return task[0]

@app.post("/task/")
async def create_task(task: Task):
    if [t for t in tasks if t.id==task.id]:
        raise HTTPException(status_code=409, detail="Task already exists")
    tasks.append(task)
    return task

@app.put("/task/")
async def update_tasks(task: Task):
    for ind in range(len(tasks)):
        if tasks[ind].put == task.id:
            tasks[ind] = task
            return tasks[ind]
    raise HTTPException(status_code=404, detail="Task did not found")

@app.delete("/task/")
async def delete_tasks(id: int):
    for ind in range(len(tasks)):
        if tasks[ind].id == id:
            tasks.pop(ind)
            return {'message':'Task deleted'}
    raise HTTPException(status_code=404, detail="Task not found")