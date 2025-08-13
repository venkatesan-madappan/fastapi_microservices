from fastapi import FastAPI
from contextlib import asynccontextmanager

from config.db.db_setup import Base

from config.db.db_setup import async_engine, async_session

from models.data import nsms

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup code ---
    print("App starting up...")

    app.state.engine = async_engine
    app.state.async_session = async_session

    #Optional : create tables on startup
    async with app.state.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # e.g. connect to DB, load models, etc.
    
    yield  # App runs while paused here

    # --- Shutdown code ---
    print("App shutting down...")
    # e.g. close DB connections, cleanup
	