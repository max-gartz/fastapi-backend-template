"""Main module for creating and starting FastAPI app."""
import os
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI
from gunicorn import glogging

from app import __api_title__, __description__, __version__
from app.api.auth import auth_router
from app.api.chats import chats_router
from app.api.users import users_router
from app.config import settings
from app.utils.logging import get_logging_config, setup_logging, shutdown_logging


class CustomGunicornLogger(glogging.Logger):
    """Custom Gunicorn logger."""

    def setup(self, cfg: Dict[str, Any]) -> None:
        """Setup logger."""
        setup_logging(config_path=settings.logger.config_path)


@asynccontextmanager
async def lifespan(_: FastAPI):  # type: ignore
    """Context manager for app startup and shutdown."""
    setup_logging(config_path=settings.logger.config_path)
    yield
    shutdown_logging()


root = FastAPI(
    title=__api_title__,
    description=__description__,
    version=__version__,
    lifespan=lifespan
)

root.include_router(auth_router.router)
root.include_router(users_router.router)
root.include_router(chats_router.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="app.main:root",
        host=os.environ.get("HOST", "127.0.0.1"),
        port=os.environ.get("PORT", 8080),
        log_config=get_logging_config(config_path=settings.logger.config_path),
        reload=True
    )
