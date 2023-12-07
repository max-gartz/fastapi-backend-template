"""Main module for creating and starting FastAPI app."""
import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app import __api_title__, __description__, __version__
from app.api.examples import examples_router


def setup_logging() -> None:
    """Setup logging."""
    ...


def shutdown_logging(logger: logging.Logger) -> None:
    """Shutdown logging"""
    logger.info("Shutting down...")
    logging.shutdown(logger.handlers)


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore
    """Context manager for app startup and shutdown."""
    setup_logging()
    yield
    shutdown_logging(logging.getLogger())


root = FastAPI(
    title=__api_title__,
    description=__description__,
    version=__version__,
    lifespan=lifespan
)

root.include_router(examples_router.router)

if __name__ == "__main__":
    uvicorn.run(
        app="app.main:root",
        host="127.0.0.1",
        port=8080,
        log_level="info",
        reload=True
    )
