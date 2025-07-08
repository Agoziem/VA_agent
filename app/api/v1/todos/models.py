import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, String, JSON, Enum as SQLAEnum
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class TodoStatus(str, Enum):
    """Enum for Todo status."""
    PENDING = "pending"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Todo(Base):
    """Todo model."""
    __tablename__ = "todos"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[TodoStatus] = mapped_column(SQLAEnum(TodoStatus), default=TodoStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    collection_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("todo_collections.id"), nullable=True)
    collection: Mapped["TodoCollection"] = relationship("TodoCollection", back_populates="todos")

    # user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    # user: Mapped["User"] = relationship("User", back_populates="todos")  # Assuming User model exists

class TodoCollection(Base):
    """TodoCollection model."""
    __tablename__ = "todo_collections"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    todos: Mapped[List[Todo]] = relationship("Todo", back_populates="collection", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TodoCollection(id={self.id}, name={self.name})>"