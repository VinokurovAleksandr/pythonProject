from pydantic import BaseModel, Field

class UpsertTask(BaseModel):
    name: str = Field(...,min_length=3,max_length=50)
    status: str = Field(...,min_length=3,max_length=50)
    term: str = Field(min_length=3,max_length=50)
    description: str = Field(min_length=3,max_length=50)
