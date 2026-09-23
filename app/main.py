from fastapi import FastAPI

from app.api.rag import router as rag_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name
)


app.include_router(rag_router)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }