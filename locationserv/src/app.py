import logging.config
from contextlib import asynccontextmanager
from fastapi import FastAPI
# Imports from within the project
from config import cfg
from src.routes import router
from src.db import init_db, get_db, client, ensure_indexes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logging.config.dictConfig(cfg.LOG_CONFIG)
    init_db()
    db = get_db()
    await ensure_indexes(db)
    
    yield
    
    # Shutdown
    if client:
        client.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Location Microservice",
        lifespan=lifespan
    )
    
    # Routes
    app.include_router(router)
    
    return app