import tracemalloc
# from typing import Union
import asyncio
import traceback

from fastapi import FastAPI, HTTPException, status

from database import (fetch_task, create_task, update_task, delete_task, create_database, create_table, drop_table)
from task import Task
from upsert_task import UpsertTask



app = FastAPI()

# async def main():
#     await create_database("mydatabase")
#     await create_table()
@app.post("/task/", response_model=Task)
async def add_task(task: UpsertTask) -> Task:
    '''
    Endpoint for adding a new task.
    :param: task: Task object to be added.
    :return: The added task object.
    :raise:  If an error occurs while creating the task.
    '''
    try:
        created_task = await create_task(task)
        return created_task
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))


@app.get("/task/{id}", response_model=Task)
async def get_task(task_id: int) -> Task:
    '''
    Getting a task by its id.
    :param task_id: id of the task.
    :return: Task object with given id.
    '''
    if task_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Task ID must be greater than 0")
    tasks = await fetch_task()
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Task not found")


@app.put("/task/{id}", response_model=Task)
async def update_task_id(id: int, task: UpsertTask) -> Task:
    '''
    Updating a task by its id.
    :param id: id of the task.
    :param task: Task object to be updated.
    :return: The update task object by its id.
    :raise: If the task with the specified is not found or
            no change were made during the update
    '''
    if id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Task ID must be greater than 0")
    try:
        updated_task, task_id = await update_task(id, task)
        if updated_task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found or changes were made")
        return Task(id=task_id, **updated_task.dict())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))


@app.delete("/task/{task_id}", response_model=Task)
async def delete_task_id(task_id: int) -> Task:
    '''
    Deleting a task by its id
    :param task_id(int): The id of the task to be delete
    :return: The  deleted task object.
    :raise: If the task with the specified is not found or
            ID must be greater than 0
    '''
    if task_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Task ID must be greater than 0")
    tasks = await fetch_task()
    for task in tasks:
        if task.id == task_id:
            await delete_task(task_id)
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Task not found")




tracemalloc.start()
# async def main():
    # await create_database("mydatabase")
    # await create_table()
    # await drop_table()

# asyncio.run(main())

