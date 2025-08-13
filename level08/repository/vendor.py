from models.data.nsms import Vendor, Login
from models.request.vendor import VendorReq
from datetime import date, time
from typing import List, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class VendorRepository:    
    async def insert_vendor(self, req:VendorReq, db:AsyncSession) -> bool: 
        vendor_l = Vendor(id=req.id, rep_firstname=req.rep_firstname, rep_lastname=req.rep_lastname,\
                          rep_id=req.rep_id, rep_date_employed=req.rep_date_employed, \
                            account_name=req.account_name, account_number=req.account_number,\
                                  date_consigned=req.date_consigned,\
                                      login_id=req.login_id)
        try:
            db.add(vendor_l)
            await db.commit()
            return True
        except Exception as e: 
            print(e)
            await db.rollback()
            return False 
    
    async def update_vendor(self, id:int, details:Dict[str, Any]) -> bool: 
        pass
   
    async def delete_vendor(self, id:int) -> bool: 
        pass

    
    async def get_all_vendor(self, db:AsyncSession):
        try:
            q_result = await db.execute(select(Vendor))
            vendor_qr = q_result.scalars().all()
            return vendor_qr
        except Exception as e:
            print(e)
            return None
       
    async def get_vendor(self, db: AsyncSession): 
        try:
            q_result = await db.execute(select(Vendor))
            vendor_qr = q_result.scalars().all()
            return vendor_qr
        except Exception as e:
            print(e)
            return None



    
