
FROM python:3.12.0

#WORKDIR . /app

#COPY ../requirements.txt .
RUN pip install fastapi uvicorn aioodbc pyodbc

#RUN pip install -r ./requirements.txt

COPY . /app

WORKDIR /app

CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]
