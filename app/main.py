from fastapi import FastAPI
from app.core.routes import router as main_router
# from app.core.middleware import register_middleware
from contextlib import asynccontextmanager
from fastapi_mcp import FastApiMCP
from fastapi.routing import APIRoute

description = """
Virtual Assistant Agent API allows you to interact with a virtual assistant that can perform various tasks such as searching the web, managing tasks, and more.
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    This is used to initialize resources when the app starts and clean them up when it stops.
    """
    mcp = FastApiMCP(app, include_tags=["todos"])
    mcp.mount()
    print("MCP mounted successfully")
    yield

app = FastAPI(
    title="VA Agent API",
    description=description,
    version="0.1.0",
    lifespan=lifespan,
)

# Include your main app routes
app.include_router(main_router, prefix="/api/v1")

# Register custom middleware
# register_middleware(app)


# Root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the VA Agent API!"}


