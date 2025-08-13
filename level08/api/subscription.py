from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.request.subscription import SubscriptionReq
from models.data.nsms import Customer, Subscription
from repository.subscription import SubscriptionRepository
from config.db.db_setup import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import date
router = APIRouter()

@router.post("/subscription/add", )
async def add_subscription(req: SubscriptionReq, db:AsyncSession=Depends(get_async_session)):
    repo = SubscriptionRepository()
    result = await repo.insert_subscription(req=req, db=db)
    if result == True: 
        return req 
    else: 
        return JSONResponse(content={'message':'update trainer profile problem encountered'}, status_code=500)

@router.get("/subscription/list/all")
async def list_all_subscriptions():
    repo = SubscriptionRepository()
    result = await repo.get_all_subscription();
    if result:
        return result
    else:
        return JSONResponse(content={'message':'Subscription List problem encountered'}, status_code=500)

#TO-DO
@router.post("/subscription/dated")
async def list_dated_subscription(min_date:date, max_date:date):
    pass
#TO-DO
@router.get("/subscription/monitor/total")
async def list_all_customer_subscription():
    pass
