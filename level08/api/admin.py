from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from models.request.admin import AdminReq
from models.data.nsms import Admin
from config.db.db_setup import get_async_session
from repository.admin import AdminRepository, AdminLoginRepository, BillingAdminRepository
from services.admin import process_billing


router = APIRouter()

@router.post("/admin/add")
async def add_admin_coroutine(req: AdminReq, db: AsyncSession=Depends(get_async_session)):
    admin_r = AdminRepository()
    result = await admin_r.insert_admin(req=req, db=db)
    # result = await admin_r.insert_admin(req=req, db=db)
    if result == True: 
        return req
    else: 
        return JSONResponse(content={'message':'Admin add profile problem encountered'}, status_code=500)

@router.post("/admin/login/list")
async def list_admin_login(db:AsyncSession=Depends(get_async_session)):
    repo = AdminRepository()
    result = await repo.list_all_admin(db=db)
    return result
    #  repo = AdminLoginRepository()
    #  result = await repo.join_login_admin(db=db)
    #  return jsonable_encoder(result)

#TO-DO
@router.get("/admin/billing/all")
async def list_admin_with_billing(db:AsyncSession=Depends(get_async_session)):
     repo = BillingAdminRepository()
     result = await repo.join_admin_billing(db=db)
     data = await process_billing(result)
     return data
    #  for rec in result:
    #      print(jsonable_encoder(rec[0]), jsonable_encoder(rec[1]))



#TO-DO - as of now we can skip this
@router.get("/admin/login/list/enc")
async def generate_encypted_profile(db:AsyncSession=Depends(get_async_session)):
     repo = AdminLoginRepository()
     result = await repo.join_login_admin()
     return jsonable_encoder(result)
     

