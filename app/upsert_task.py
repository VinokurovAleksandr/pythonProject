from pydantic import BaseModel, Field, ValidationError

class UpsertTask(BaseModel):
    name: str = Field(...,min_length=3,max_length=50)
    status: str = Field(...,min_length=3,max_length=50)
    term: str = Field(min_length=3,max_length=50)
    description: str = Field(min_length=3,max_length=50)

try:
    task = UpsertTask(name='Task Name', status='Status', term='Term', description='Description')
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))