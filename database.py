import pyodbc
import aioodbc
from typing import List

import task
from task import Task

server = '127.0.0.1,1433'
database = 'master'
username = 'sa'
password = 'P@s5w0rd'
driver = '{ODBC Driver 18 for SQL Server}'

table_name = "Tasks"

async def get_connection():
    conn = await aioodbc.connect(dsn=f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes')
    conn.autocommit = True
    return conn


async def create_database(database_name):
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
    async with await get_connection() as conn:
        cursor = await conn.cursor()
        await cursor.execute(f'INSERT INTO {table_name} (id, name, status, term, description) VALUES (?, ?, ?, ?, ?)',
                        (task.id, task.name, task.status, task.term, task.description))
        await conn.commit()
    return task

async def fetch_task() -> List[Task]:
    async with await get_connection() as conn:
        cursor = await conn.cursor()
        await cursor.execute(f'SELECT * FROM {table_name}')
        tasks = await cursor.fetchall()
    return [Task(id=row[0], name=row[1], status=row[2], term=row[3], description=row[4]) for row in tasks]



async def update_task(task: Task):
    async with await get_connection() as conn:
        cursor = await conn.cursor()
        await cursor.execute(f'UPDATE {table_name} SET name = ?, status = ?, term = ?, description = ? WHERE id = ?',
                       (task.name, task.status, task.term, task.description, task.id))
        await cursor.commit()
    return task

async def delete_task(task_id: int) -> Task:
    async with await get_connection() as conn:
        cursor = await conn.cursor()
        await cursor.execute(f'DELETE FROM {table_name} WHERE id = ?', (task_id,))
        await cursor.commit()
    return Task(id=task_id, name='', status='', term='', description='')


# Create BD
#cursor.execute('CREATE DATABASE mydatabase')
#print("Database created successfully")

#Create TABLE

#cursor.execute('CREATE TABLE Tasks ( ID INT PRIMARY KEY NOT NULL, Name VARCHAR(50) NOT NULL, Status VARCHAR(50), Term VARCHAR(50), Description VARCHAR(255))')
#cursor.commit()
#print("Table Created")








