from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.api.v1.todos.models import (
    Todo,
    TodoCollection,
)
from app.api.v1.todos.schemas import (
    TodoCreate,
    TodoUpdate,
    TodoInDB,
    TodoResponse,
    TodoCollectionBase,
    TodoCollectionCreate,
    TodoCollectionUpdate,
    TodoCollectionInDB,
    TodoCollectionResponse,
)


class TodoService:
    """Service class for Todo operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_todo_by_id(self, todo_id: UUID) -> Optional["Todo"]:
        """Get a Todo by its ID."""
        stmt = select(Todo).where(Todo.id == todo_id).options(
            selectinload(Todo.collection))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_todo(self, todo_create: TodoCreate) -> TodoInDB:
        """Create a new Todo."""
        print("Creating Todo with data:")
        print(todo_create)
        todo = Todo(
            title=todo_create.title,
            description=todo_create.description,
            status=todo_create.status,
            collection_id=todo_create.collection_id,
        )
        self.db.add(todo)
        await self.db.commit()
        await self.db.refresh(todo)
        return TodoInDB.model_validate(todo)

    async def update_todo(self, todo_id: UUID, todo_update: TodoUpdate) -> Optional[TodoInDB]:
        """Update an existing Todo."""
        result = await self.db.execute(
            select(Todo)
            .where(Todo.id == todo_id)
        )
        todo = result.scalar_one_or_none()
        if not todo:
            return None
        for key, value in todo_update.model_dump(exclude_unset=True).items():
            setattr(todo, key, value)
        await self.db.commit()
        await self.db.refresh(todo)
        return TodoInDB.model_validate(todo)

    async def delete_todo(self, todo_id: UUID) -> bool:
        """Delete a Todo by its ID."""
        result = await self.db.execute(
            select(Todo).where(Todo.id == todo_id)
        )
        todo = result.scalar_one_or_none()
        if not todo:
            return False
        await self.db.delete(todo)
        await self.db.commit()
        return True

    async def get_all_todos(self) -> list[TodoResponse]:
        """Get all Todos."""
        result = await self.db.execute(
            select(Todo).options(selectinload(Todo.collection))
        )
        todos = result.scalars().all()
        return [TodoResponse.model_validate(todo) for todo in todos]

    async def get_todos_by_collection_id(self, collection_id: UUID) -> list[TodoResponse]:
        """Get all Todos in a specific collection."""
        result = await self.db.execute(
            select(Todo).where(Todo.collection_id == collection_id).options(
                selectinload(Todo.collection))
        )
        todos = result.scalars().all()
        return [TodoResponse.model_validate(todo) for todo in todos]

    
class TodoCollectionService:
    """Service class for TodoCollection operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_collection_by_id(self, collection_id: UUID) -> Optional[TodoCollectionResponse]:
        """Get a TodoCollection by its ID."""
        stmt = select(TodoCollection).options(
            selectinload(TodoCollection.todos)
        ).where(TodoCollection.id == collection_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_collection(self, collection_create: TodoCollectionCreate) -> TodoCollectionInDB:
        """Create a new TodoCollection."""
        collection = TodoCollection(
            name=collection_create.name,
            description=collection_create.description,
        )
        self.db.add(collection)
        await self.db.commit()
        await self.db.refresh(collection)
        return TodoCollectionInDB.model_validate(collection)

    async def update_collection(self, collection_id: UUID, collection_update: TodoCollectionUpdate) -> Optional[TodoCollectionInDB]:
        """Update an existing TodoCollection."""
        result = await self.db.execute(
            select(TodoCollection).where(TodoCollection.id == collection_id)
        )
        collection = result.scalar_one_or_none()
        if not collection:
            return None
        for key, value in collection_update.model_dump(exclude_unset=True).items():
            setattr(collection, key, value)
        await self.db.commit()
        await self.db.refresh(collection)
        return TodoCollectionInDB.model_validate(collection)

    async def delete_collection(self, collection_id: UUID) -> bool:
        """Delete a TodoCollection by its ID."""
        result = await self.db.execute(
            select(TodoCollection).where(TodoCollection.id == collection_id)
        )
        collection = result.scalar_one_or_none()
        if not collection:
            return False
        await self.db.delete(collection)
        await self.db.commit()
        return True

    async def get_all_collections(self) -> list[TodoCollectionInDB]:
        """Get all TodoCollections."""
        result = await self.db.execute(select(TodoCollection))
        collections = result.scalars().all()
        return [TodoCollectionInDB.model_validate(collection) for collection in collections]