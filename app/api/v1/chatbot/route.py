from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from .service import VAServices

va_router = APIRouter()
va_service = VAServices()


@va_router.get("/{message}")
async def chat_stream(message: str, checkpoint_id: Optional[str] = None):
    """
    streams response to the user in real-time as the AI model generates it.
    """
    print("Received message:", message)
    try:
        return StreamingResponse(
            va_service.generate_chat_response(message, checkpoint_id),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
