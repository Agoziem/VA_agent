# server.py
from typing import Optional, Annotated
from mcp.server.fastmcp import FastMCP
from app.api.v1.todos.services import TodoService, TodoCollectionService
from app.core.database import async_get_db
from app.api.v1.todos.schemas import (
    TodoCreate, TodoUpdate, TodoInDB,
    TodoCollectionCreate, TodoCollectionUpdate, TodoStatus
)
from uuid import UUID

# Create an MCP server
mcp = FastMCP("Todo Server")

# ------------------ TODO TOOLS ------------------


@mcp.tool()
async def create_todo_tool(
    title: str,
    description: str = "",
    collection_id: str = "",
    status: str = "pending",
) -> Optional[dict]:
    """Create a new Todo item."""
    async for session in async_get_db():
        service = TodoService(session)
        todo = await service.create_todo(TodoCreate(
            title=title,
            description=description,
            status=TodoStatus(status) if status else TodoStatus.PENDING,
            collection_id=UUID(collection_id) if collection_id else None
        ))
        if not todo:
            raise ValueError("Failed to create Todo")
        return todo.model_dump()


@mcp.tool()
async def update_todo_tool(
    todo_id: str,
    title: str = "",
    description: str = "",
    status: str = "",
    collection_id: str = ""
) -> Optional[dict]:
    """Update a Todo item by its ID."""
    async for session in async_get_db():
        service = TodoService(session)
        todo = await service.update_todo(
            UUID(todo_id),
            TodoUpdate(
                title=title if title else None,
                description=description if description else None,
                status=TodoStatus(status) if status else None,
                collection_id=UUID(collection_id) if collection_id else None
            )
        )
        if not todo:
            raise ValueError("Todo not found")
        return todo.model_dump()


@mcp.tool()
async def get_todo_tool(todo_id: str) -> Optional[dict]:
    """Retrieve a single Todo item by ID."""
    async for session in async_get_db():
        service = TodoService(session)
        todo = await service.get_todo_by_id(UUID(todo_id))
        if not todo:
            raise ValueError("Todo not found")
        return TodoInDB.model_validate(todo).model_dump()


@mcp.tool()
async def delete_todo_tool(todo_id: str) -> Optional[bool]:
    """Delete a Todo by ID."""
    async for session in async_get_db():
        service = TodoService(session)
        deleted = await service.delete_todo(UUID(todo_id))
        if not deleted:
            raise ValueError("Todo not found")
        return True


# ------------------ COLLECTION TOOLS ------------------ #

@mcp.tool()
async def create_collection_tool(
    name: str,
    description: str = "",
) -> Optional[dict]:
    """Create a new Todo collection."""
    async for session in async_get_db():
        service = TodoCollectionService(session)
        collection = await service.create_collection(TodoCollectionCreate(
            name=name,
            description=description if description == "" else None
        ))
        if not collection:
            raise ValueError("Failed to create collection")
        return collection.model_dump()


@mcp.tool()
async def update_collection_tool(
    collection_id: str,
    name: str = "",
    description: str = ""
) -> Optional[dict]:
    """Update a Todo collection."""
    async for session in async_get_db():
        service = TodoCollectionService(session)
        collection = await service.update_collection(
            UUID(collection_id),
            TodoCollectionUpdate(
                name=name if name else None,
                description=description if description else None
            )
        )
        if not collection:
            raise ValueError("Collection not found")
        return collection.model_dump()


@mcp.tool()
async def delete_collection_tool(collection_id: str) -> Optional[bool]:
    """Delete a collection by ID."""
    async for session in async_get_db():
        service = TodoCollectionService(session)
        return await service.delete_collection(UUID(collection_id))


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
