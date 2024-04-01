from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Task(BaseModel):
    id: str
    author: str 
    deadline: str 
    title: str 
    description: str


# class Task(Base):
#     __tablename__ = "tasks"

#     id = Column(Integer, primary_key=True, index=True)
#     author = Column(String)
#     deadline = Column(String)
#     title = Column(String)     
#     description = Column(String)     
    

