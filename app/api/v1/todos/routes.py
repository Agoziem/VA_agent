from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.api.v1.todos.schemas import (
    TodoCreate,
    TodoUpdate,
    TodoInDB,
    TodoResponse,
    TodoCollectionCreate,
    TodoCollectionUpdate,
    TodoCollectionInDB,
    TodoCollectionResponse,
)
from app.api.v1.todos.services import TodoService, TodoCollectionService
from app.core.database import async_get_db  # Assuming you have a session provider

todo_router = APIRouter()


# ----------- TODO ROUTES -----------

@todo_router.get("/", response_model=List[TodoResponse])
async def get_all_todos(session: AsyncSession = Depends(async_get_db)):
    service = TodoService(session)
    return await service.get_all_todos()


@todo_router.get("/{todo_id}", response_model=TodoInDB)
async def get_todo(todo_id: UUID, session: AsyncSession = Depends(async_get_db)):
    service = TodoService(session)
    todo = await service.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@todo_router.post("/", response_model=TodoInDB, status_code=status.HTTP_201_CREATED)
async def create_todo(todo_create: TodoCreate, session: AsyncSession = Depends(async_get_db)):
    service = TodoService(session)
    return await service.create_todo(todo_create)


@todo_router.put("/{todo_id}", response_model=TodoInDB)
async def update_todo(todo_id: UUID, todo_update: TodoUpdate, session: AsyncSession = Depends(async_get_db)):
    service = TodoService(session)
    todo = await service.update_todo(todo_id, todo_update)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@todo_router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: UUID, session: AsyncSession = Depends(async_get_db)):
    service = TodoService(session)
    success = await service.delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")


@todo_router.get("/collection/{collection_id}", response_model=List[TodoResponse])
async def get_todos_by_collection(collection_id: UUID, session: AsyncSession = Depends(async_get_db)):
    service = TodoService(session)
    return await service.get_todos_by_collection_id(collection_id)


# ----------- COLLECTION ROUTES -----------

@todo_router.get("/collections/", response_model=List[TodoCollectionResponse])
async def get_all_collections(session: AsyncSession = Depends(async_get_db)):
    service = TodoCollectionService(session)
    return await service.get_all_collections()


@todo_router.get("/collections/{collection_id}", response_model=TodoCollectionInDB)
async def get_collection(collection_id: UUID, session: AsyncSession = Depends(async_get_db)):
    service = TodoCollectionService(session)
    collection = await service.get_collection_by_id(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@todo_router.post("/collections/", response_model=TodoCollectionInDB, status_code=status.HTTP_201_CREATED)
async def create_collection(collection: TodoCollectionCreate, session: AsyncSession = Depends(async_get_db)):
    service = TodoCollectionService(session)
    return await service.create_collection(collection)


@todo_router.put("/collections/{collection_id}", response_model=TodoCollectionInDB)
async def update_collection(collection_id: UUID, collection_update: TodoCollectionUpdate, session: AsyncSession = Depends(async_get_db)):
    service = TodoCollectionService(session)
    updated = await service.update_collection(collection_id, collection_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Collection not found")
    return updated


@todo_router.delete("/collections/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(collection_id: UUID, session: AsyncSession = Depends(async_get_db)):
    service = TodoCollectionService(session)
    success = await service.delete_collection(collection_id)
    if not success:
        raise HTTPException(status_code=404, detail="Collection not found")
