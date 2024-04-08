from typing import List
from typing import Union

import aioodbc
import pyodbc

from task import Task

server = '127.0.0.1,1433'
database = 'master'
username = 'sa'
password = 'P@s5w0rd'
driver = '{ODBC Driver 18 for SQL Server}'

table_name = "Tasks"


async def get_connection() -> aioodbc.Connection:
    conn = await aioodbc.connect(
        dsn=f'DRIVER={driver};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password};'
            f'TrustServerCertificate=yes')
    conn.autocommit = True
    return conn


async def create_database(database_name: str) -> None:
    '''
    Creates the database
    :param database_name: Name of the database
    '''
    conn = await get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f'CREATE DATABASE {database_name}')
        print("Database created successfully")
    except pyodbc.Error as e:
        print(f"Error creating database: {e}")
    finally:
        conn.close()


async def create_task(task: Task) -> Task:
    '''
    Create a task in the database
    :param task: The task object to be created
    :return: The created task object
    '''
    async with await get_connection() as conn:
        cursor = await conn.cursor()
        await cursor.execute(
            f'INSERT INTO {table_name} (id, name, status, term, description) VALUES (?, ?, ?, ?, ?)',
            (task.id,
             task.name,
             task.status,
             task.term,
             task.description))
        await conn.commit()
    return task


async def fetch_task() -> List[Task]:
    '''
    Fetch task in the database
    :return: List[Task] A list of task objects
    '''
    async with await get_connection() as conn:
        cursor = await conn.cursor()
        await cursor.execute(f'SELECT * FROM {table_name}')
        tasks = await cursor.fetchall()
    return [Task(id=row[0],
                 name=row[1],
                 status=row[2],
                 term=row[3],
                 description=row[4])
            for row in tasks]


async def update_task(task_id: Union[int, str], task: Task) -> Task:
    '''
    Update a task in the database
    :param task_id: Id of the task to be updated
    :param task: The task to be updated
    :return:  The updated task object
    '''
    async with await get_connection() as conn:
        cursor = await conn.cursor()
        await cursor.execute(f'UPDATE {table_name} SET name = ?, status = ?, term = ?, description = ? WHERE id = ?',
                             (task.name, task.status, task.term, task.description, task_id))
        await cursor.commit()
    return task


async def delete_task(task_id: int) -> Task:
    '''
    Delete a task in the database
    :param task_id: Id of the task to be deleted
    :return:  The deleted task object
    '''
    async with await get_connection() as conn:
        cursor = await conn.cursor()
        await cursor.execute(f'DELETE FROM {table_name} WHERE id = ?',
                             (task_id,))
        await cursor.commit()
    return Task(id=task_id, name='', status='', term='', description='')

# Create BD
# cursor.execute('CREATE DATABASE mydatabase')
# print("Database created successfully")

# Create TABLE

# cursor.execute('CREATE TABLE Tasks ( ID INT PRIMARY KEY NOT NULL, Name VARCHAR(50) NOT NULL, Status VARCHAR(50), Term VARCHAR(50), Description VARCHAR(255))')
# cursor.commit()
# print("Table Created")
