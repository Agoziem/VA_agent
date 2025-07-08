from fastapi import APIRouter
from app.api.v1.chatbot.route import va_router
from app.api.v1.todos.routes import todo_router

router = APIRouter()

router.include_router(
    va_router,
    prefix="/chatbot",
    tags=["agentic chatbot"]
)
router.include_router(
    todo_router,
    prefix="/todos",
    tags=["todos"]
)