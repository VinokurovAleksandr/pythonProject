from fastapi import FastAPI, HTTPException, status
from typing import Union

from database import fetch_task, create_task, update_task, delete_task
from task import Task
import tracemalloc

app = FastAPI()

@app.post("/task/", response_model=Task)
async def add_task(task: Task) -> Task:
    try:
        await create_task(task)
        return task
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))

@app.get("/task/{id}", response_model=Task)
async def get_task(task_id: int) -> Task:
    tasks = await fetch_task()
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Task not found")

@app.put("/task/{id}", response_model=Task)
async def update_task_id(task_id: Union[int, str], task: Task) -> Task:
    try:
        update_rows = await update_task(task_id, task)
        if update_rows == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found or changes were made")
        return task
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))

@app.delete("/task/{task_id}", response_model=Task)
async def delete_task_id(task_id:int) -> Task:
    tasks = await fetch_task()
    for task in tasks:
        if task.id == task_id:
            await delete_task(task_id)
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Task not found")


tracemalloc.start()
