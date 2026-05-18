from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.api import research, plugins, export, config


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Deep Research",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(research.router, prefix="/api")
app.include_router(plugins.router, prefix="/api")
app.include_router(export.router, prefix="/api")
app.include_router(config.router, prefix="/api")


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
