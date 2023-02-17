from dataclasses import Field

from pydantic import BaseModel
from typing import List, Optional

from sqlmodel import SQLModel, Field, Column, JSON


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    image: str
    description: str
    location: str
    tags: List[str] = Field(sa_column=Column(JSON))

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            'example': {
                'title': 'FastApi Book Launch',
                'image': 'https://linktomyimage.com/image.png',
                'description': 'we will be',
                'tags': ['python', 'fastapi', 'book', 'launch'],
                'location': 'google meet'
            }
        }


class EventUpdate(SQLModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    location: Optional[str]
    tags: Optional[List[str]]

    class Config:
        schema_extra = {
            'example': {
                'title': 'fastapi',
                'image': 'https://image',
                'description': 'we will',
                'tag': ['py', 'fa', 'bk'],
                'location': 'google'
            }
        }