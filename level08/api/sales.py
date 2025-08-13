from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from rx.scheduler.eventloop import AsyncIOScheduler

from models.request.sales import SalesReq
from models.data.nsms import Sales, Publication
from repository.sales import SalesRepository
from config.db.db_setup import get_async_session
from services.sales import create_observable

import asyncio



router = APIRouter()

@router.post("/sales/add")
async def add_sales(req: SalesReq, db:AsyncSession=Depends(get_async_session)):
    repo = SalesRepository()
    result = await repo.insert_sales(req=req, db=db)
    if result == True: 
        return req 
    else: 
        return JSONResponse(content={'message':'update trainer profile problem encountered'}, status_code=500)
    
#TO-DO
@router.get("/sales/list/quota")
async def list_sales_by_quota():
    loop = asyncio.get_event_loop()
    observer = create_observable(loop)
    observer.subscribe (
        on_next = lambda value : print(f"Received instruction to buy {value}"),
        on_error =  lambda e: print(e),
        on_completed = print("Completed Trades"),
        scheduler = AsyncIOScheduler(loop)
    )

    return {"message":"Notification sent in the background"}
