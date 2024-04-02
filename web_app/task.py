from pydantic import BaseModel

class Task(BaseModel):
    id: str
    author: str 
    deadline: str 
    title: str 
    description: str



    

