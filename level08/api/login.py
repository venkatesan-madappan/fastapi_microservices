

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from models.request.login import LoginReq
from config.db.db_setup import get_async_session
from repository.login import LoginRepository
from services.login import build_user_list, count_login

import asyncio
    
router = APIRouter()

@router.post("/login/add")
async def add_login_coroutine(req: LoginReq, db:AsyncSession = Depends(get_async_session)):
    lr = LoginRepository()
    result = await lr.insert_login(req, db)
    if result== True: 
        return req
    else: 
        return JSONResponse(content={'message':'insert login profile problem encountered'}, status_code=500)

#TO-DO : Need to work on this the select query is not working
@router.post("/login/update")    
async def update_login_coroutine(req:LoginReq, db:AsyncSession = Depends(get_async_session)):
    lr = LoginRepository()
    result = await lr.update_login(lreq=LoginReq, db=db)
    if result== True: 
        return req
    else: 
        return JSONResponse(content={'message':'update login profile problem encountered'}, status_code=500)    

@router.get("/login/list/all")
async def get_all_users(db: AsyncSession = Depends(get_async_session)):
    print(f"Lets see the type of db {type(db)}")
    lr = LoginRepository()
    result = await lr.get_all_login(db=db)
    req = jsonable_encoder(result)
    if result: 
        return req
    else: 
        return JSONResponse(content={'message':'List All Login profile problem encountered'}, status_code=500)
    

@router.get("/login/list/records")
async def list_login_records(db: AsyncSession = Depends(get_async_session)):
    lr = LoginRepository()
    result = await lr.get_all_login(db=db)
    req = await asyncio.gather(count_login(result), build_user_list(result))
    if result: 
        return req
    else: 
        return JSONResponse(content={'message':'List All Records problem encountered'}, status_code=500)
