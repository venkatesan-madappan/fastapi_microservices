from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from models.request.customer import CustomerReq
from models.data.nsms import Customer, Login

from repository.customer import CustomerRepository
from config.db.db_setup import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.post("/customer/add")
async def add_customer(req: CustomerReq, db:AsyncSession=Depends(get_async_session)):
    repo = CustomerRepository()
    result = await repo.insert_customer(req=req, db=db)
    if result == True: 
        return req 
    else: 
        return JSONResponse(content={'message':'customer add problem encountered'}, status_code=500)
    

#TO-DO
# @router.websocket("/customer/list/ws")
# async def customer_list_ws(websocket: WebSocket):
# 	pass
#TO-DO
@router.get("/customer/wsclient/list/")  
async def customer_list_ws_client():
	pass