from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from models.request.billing import BillingReq

from config.db.db_setup import get_async_session
from models.data.nsms import Billing
from repository.billing import BillingRepository, BillingVendorRepository
from services.billing import generate_billing_sheet, create_total_payables_year

from datetime import date
router = APIRouter()

@router.post("/billing/add/")
async def billing_add(req: BillingReq, db: AsyncSession = Depends(get_async_session)):
    billing_r = BillingRepository()
    result = await billing_r.billing_insert(req=req, db=db)
    if result==True:
        return req
    else:
        JSONResponse(content={"message":"Failed to add the Billing request"}, status_code=500)

@router.post("/billing/list/")
async def billing_delete(db:AsyncSession = Depends(get_async_session)):
    bill_l = BillingRepository()
    result = await bill_l.get_all_billing(db=db)
    req = jsonable_encoder(result)
    if result: 
        return req
    else: 
        return JSONResponse(content={'message':'List All Billing  problem encountered'}, status_code=500)

@router.post("/billing/delete/")
async def billing_delete(id:int, db:AsyncSession = Depends(get_async_session)):
    pass
	

@router.post("/billing/save/csv")
async def save_vendor_billing(billing_date:date, tasks: BackgroundTasks, db:AsyncSession=Depends(get_async_session)):
    try:
        bill_r = BillingVendorRepository()
        vendor_billing_join_data = await bill_r.join_billing_vendor(bill_date=billing_date, db=db)
        print(vendor_billing_join_data)
        # await generate_billing_sheet(billing_date, vendor_billing_join_data)
        tasks.add_task(generate_billing_sheet, billing_date, vendor_billing_join_data)
        return JSONResponse(content={"message":"Successfully written to csv file"}, status_code = 200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"message":"Something wrong in writting csv file"}, status_code = 500)

#TO-DO
@router.post("/billing/total/payable")
async def compute_payables_yearly(billing_date:date):
    try:
        bill_r = BillingVendorRepository()
        vendor_billing_join_data = await bill_r.join_billing_vendor(bill_date=billing_date, db=db)
        print(vendor_billing_join_data)
        await create_total_payables_year(billing_date, vendor_billing_join_data)
        return JSONResponse(content={"message":"Successfully completed compute_payables_yearly"}, status_code = 200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"message":"Something wrong in compute_payables_yearly"}, status_code = 500)


