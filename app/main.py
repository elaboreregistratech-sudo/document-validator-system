from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import get_settings
from app.seed import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="API para validação documental, regras de negócio, trilha de auditoria e workflows operacionais.",
    lifespan=lifespan,
)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "environment": settings.app_env}


app.include_router(api_router, prefix="/api/v1")
