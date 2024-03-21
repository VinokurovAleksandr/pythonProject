from pydantic import BaseModel

class Task(BaseModel):
    id: int
    name: str
    status: str
    term: str
    description: str