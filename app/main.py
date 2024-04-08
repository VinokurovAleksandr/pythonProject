import tracemalloc
from typing import Union

from fastapi import FastAPI, HTTPException, status

from database import fetch_task, create_task, update_task, delete_task
from task import Task

app = FastAPI()


@app.post("/task/", response_model=Task)
async def add_task(task: Task) -> Task:
    '''
    Endpoint for adding a new task.
    :param: task: Task object to be added.
    :return: The added task object.
    :raise:  If an error occurs while creating the task.
    '''
    try:
        await create_task(task)
        return task
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
async def update_task_id(task_id: Union[int, str], task: Task) -> Task:
    '''
    Updating a task by its id.
    :param task_id: id of the task.
    :param task: Task object to be updated.
    :return: The update task object by its id.
    :raise: If the task with the specified is not found or
            no change were made during the update
    '''
    if task_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Task ID must be greater than 0")
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
