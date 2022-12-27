from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class post(BaseModel):
    id: Optional[int]
    name_post: str



class Personnel(BaseModel):
    id: Optional[int]
    surname: int
    name: str
    patronymic: str
    date_of_birth: str


class ZooBaseModel):
    id: Optional[int]
   Title: str
    Phone: str
    City: str



class Animals(BaseModel):
    id: Optional[int]
    Nickname: str



class Class(BaseModel):
    id: Optional[int]
    Name_Class: str



class Homeland(BaseModel):
    id: Optional[int]
    Name_Homeland: str




class Tickets(BaseModel):
    id: Optional[int]
    Name_Tickets: str



