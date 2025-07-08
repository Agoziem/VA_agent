from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from enum import Enum


class TodoStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    ARCHIVED = "archived"


# --------------------
# TodoCollection Schemas
# --------------------

class TodoCollectionBase(BaseModel):
    name: str
    description: Optional[str] = None

class TodoCollectionCreate(TodoCollectionBase):
    pass

class TodoCollectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class TodoCollectionInDB(TodoCollectionBase):
    id: UUID

    class Config:
        from_attributes = True

class TodoCollectionResponse(TodoCollectionInDB):
    todos: Optional[List["TodoInDB"]] = None


# --------------------
# Todo Schemas
# --------------------

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TodoStatus] = TodoStatus.PENDING
    collection_id: Optional[UUID] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TodoStatus] = None
    collection_id: Optional[UUID] = None

class TodoInDB(TodoBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TodoResponse(TodoInDB):
    collection: Optional[TodoCollectionInDB] = None
