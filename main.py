from fastapi import FastAPI, HTTPException
from typing import Union
from database import fetch_task, create_task, update_task, delete_task
from task import Task
import tracemalloc

app = FastAPI()


@app.post("/task/", response_model=Task)
async def add_task(task: Task):
    await create_task(task.id, task.name, task.status, task.term, task.description)
    return task

@app.get("/task/{id}", response_model=Task)
#async def get_task(task_id: Union[int, str]):
async def get_task(task_id: int):
    tasks = await fetch_task()
    for task in tasks:
        if task[0] == task_id:
            return Task(id=task[0], name=task[1], status=task[2], term=task[3], description=task[4])
    raise HTTPException(status_code=404, detail="Task not found")




@app.put("/task/{id}", response_model=Task)
async def update_task_id(task_id: Union[int, str], task: Task):
    await update_task(task_id, task.name, task.status, task.term, task.description)
    return task

@app.delete("/task/{task_id}", response_model=Task)
async def delete_task_id(task_id:int):
    tasks = await fetch_task()
    for task in tasks:
        if task[0] == task_id:
            await delete_task(task_id)
            return Task(id=task[0], name=task[1], status=task[2], term=task[3], description=task[4])
    raise HTTPException(status_code=404, detail="Task not found")


tracemalloc.start()
