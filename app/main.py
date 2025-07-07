from fastapi import FastAPI
# from app.core.config import settings
from app.core.routes import router as main_router
from app.core.middleware import register_middleware
from contextlib import asynccontextmanager
# from app.api.v1.auth.errors import register_general_error_handlers

description = """
Virtual Assistant Agent API allows you to interact with a virtual assistant that can perform various tasks such as searching the web, managing tasks, and more.
"""


# 4. FastAPI lifespan to control broker lifecycle
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Register all errors
#     register_general_error_handlers(app)
#     yield
    

app = FastAPI(title="VA Agent API",
              description=description,
              version="0.1.0",
              )
version_prefix = f"/api/v1"
app.include_router(main_router, prefix=version_prefix)
register_middleware(app)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the VA Agent API!"}
