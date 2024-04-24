from typing import List, Tuple
from typing import Union

import aioodbc
import pyodbc

# from app.upsert_task import UpsertTask
from task import Task
from upsert_task import UpsertTask


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

async def create_task(task: UpsertTask) -> Task:
    '''
    Create a task in the database
    :param task: The task object to be created
    :return: The created task object
    '''
    async with await get_connection() as conn:
        cursor = await conn.cursor()

        await cursor.execute(
            f"IF NOT EXISTS "
            f"(SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = "
            f"'{table_name}' AND COLUMN_NAME = 'id') "
            "BEGIN "
            f"ALTER TABLE {table_name} ADD id INT IDENTITY(1,1) PRIMARY KEY "
            "END"
        )

        await cursor.execute(
            f'INSERT INTO {table_name} (name, status, term, description) VALUES (?, ?, ?, ?)',
            (task.name,
             task.status,
             task.term,
             task.description))

        await conn.commit()

        await cursor.execute(
            f"SELECT @@IDENTITY"
        )

        row = await cursor.fetchone()
        task_id = row[0] if row else None

    created_task = Task(id=task_id, **task.dict())
    return created_task


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


async def update_task(task_id: int, task: UpsertTask) -> Tuple[UpsertTask, int]:
    '''
    Update a task in the database
    :param task_id: Id of the task to be updated
    :param task: The task to be updated
    :return:  The updated task object
    '''
    async with await get_connection() as conn:
        cursor = await conn.cursor()
        await cursor.execute(
            f'UPDATE {table_name} SET name = ?, status = ?, term = ?, description = ? WHERE id = ?',
                             (task.name,
                              task.status,
                              task.term,
                              task.description,
                              task_id))
        await cursor.commit()
    return task, task_id

async def delete_task(task_id: int) -> int:
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
    return task_id


async def create_database(database_name: str):
    '''
    Creates the database
    :param database_name: Name of the database
    '''
    try:
        conn = await get_connection()
        cursor = await conn.cursor()
        await cursor.execute(f"IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = '{database_name}')"
                            "BEGIN"
                             f"CREATE DATABASE {database_name}"
                            "END")
        print("Database created successfully")
    except pyodbc.Error as e:
        print(f"Error creating database: {e}")
    finally:
        if conn:
            conn.close()

async def create_table():
    conn = await get_connection()
    cursor = await conn.cursor()
    await cursor.execute("IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Tasks' and xtype='U')"
                         "BEGIN "
                         "CREATE TABLE Tasks (ID int IDENTITY(1,1) PRIMARY KEY, "
                         "Name VARCHAR(50) NOT NULL, "
                         "Status VARCHAR(50), "
                         "Term VARCHAR(50), "
                         "Description VARCHAR(255))"
                         "END")
    cursor.commit()
    print("Table created successfully")

async def drop_table():
    '''
    Drop the Tasks table from the database
    '''
    async with await get_connection() as conn:
        cursor = await conn.cursor()
        await cursor.execute("DROP TABLE Tasks")
        await conn.commit()
        print("Table 'Tasks' dropped successfully")


 #Create BD
 #cursor.execute('CREATE DATABASE mydatabase')
 #print("Database created successfully")

# Create TABLE

 # cursor.execute('CREATE TABLE Tasks ( ID INT PRIMARY KEY NOT NULL, Name VARCHAR(50) NOT NULL, Status VARCHAR(50), Term VARCHAR(50), Description VARCHAR(255))')
 # cursor.commit()
 # print("Table Created")

