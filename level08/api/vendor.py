from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from models.request.vendor import VendorReq
from models.data.nsms import Vendor, Login
from repository.vendor import VendorRepository
from config.db.db_setup import get_async_session
  
router = APIRouter()

@router.post("/vendor/add")
async def add_vendor(req: VendorReq, db:AsyncSession = Depends(get_async_session)):
    repo = VendorRepository()
    result = await repo.insert_vendor(req=req, db=db)
    if result == True: 
        return req 
    else: 
        return JSONResponse(content={'message':'Vendor Add problem encountered'}, status_code=500)

@router.get("/vendor/list")
async def list_vendor(db:AsyncSession=Depends(get_async_session)):
    repo = VendorRepository()
    result = await repo.get_all_vendor(db=db)
    if result:
        return result
    else: 
        return JSONResponse(content={'message':'Vendor List problem encountered'}, status_code=500)
