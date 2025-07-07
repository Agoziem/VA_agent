from fastapi import APIRouter
from app.api.v1.chatbot.route import va_router

router = APIRouter()

router.include_router(
    va_router,
    prefix="/chatbot",
    tags=["agentic chatbot"]
)
