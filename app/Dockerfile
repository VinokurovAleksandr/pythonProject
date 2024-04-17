
FROM python:3.12.0

#WORKDIR . /app

#COPY ../requirements.txt .

RUN pip install fastapi uvicorn aioodbc pyodbc asyncio

#RUN pip install -r ./requirements.txt

COPY . /app

#install ms odbc
RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc
RUN curl https://packages.microsoft.com/config/ubuntu/23.04/prod.list | tee /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18

WORKDIR ./app


CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]