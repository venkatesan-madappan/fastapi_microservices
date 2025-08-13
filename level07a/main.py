from fastapi import FastAPI
from api import admin, login, profile, auction, bid

app = FastAPI()

app.include_router(admin.router, prefix="/level07")
app.include_router(login.router, prefix="/level07")
app.include_router(profile.router, prefix="/level07")
app.include_router(auction.router, prefix="/level07")
app.include_router(bid.router, prefix="/level07")

@app.get("/index")
def index(): 
    return {"content": "welcome"}
