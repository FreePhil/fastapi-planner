from typing import Optional, List
from pydantic import BaseModel, EmailStr

from models.events import Event


class User(BaseModel):
    email: EmailStr
    password: str
    events: Optional[List[Event]]

    class Config:
        schema_extra = {
            'example': {
                'email': 'fastapi@gmail.com',
                'username': 'strong!!!',
                'events': [],
            }
        }


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            'example': {
                'email': 'phil@gmail.com',
                'password': 'strong',
                'events': [],
            }
        }
