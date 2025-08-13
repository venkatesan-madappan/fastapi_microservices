from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup code ---
    print("App starting up...")
    # e.g. connect to DB, load models, etc.
    
    yield  # App runs while paused here

    # --- Shutdown code ---
    print("App shutting down...")
    # e.g. close DB connections, cleanup

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}
