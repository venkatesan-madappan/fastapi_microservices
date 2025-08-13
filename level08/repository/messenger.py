from models.data.nsms import Messenger, Vendor
from models.request.messenger import MessengerReq
from datetime import date, time
from typing import List, Dict, Any
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

class MessengerRepository: 
    
    async def insert_messenger(self, req:MessengerReq, db: AsyncSession) -> bool: 
        messenger_l = Messenger(id = req.id, firstname = req.firstname,lastname = req.lastname, \
                                salary = req.salary, date_employed = req.date_employed, 
                                status = req.status, vendor_id = req.vendor_id)
        try:
            db.add(messenger_l)
            await db.commit()
            return True
        except Exception as e: 
            print(e)
            await db.rollback()
            return False 
    
    async def update_messenger(self, id:int, details:Dict[str, Any]) -> bool: 
        pass
   
    async def delete_messenger(self, id:int) -> bool: 
        pass
    
    async def get_all_messenger(self, db:AsyncSession):
        try:
            result = await db.execute(select(Messenger))
            messenger_l = result.scalars().all()
            return messenger_l
        except Exception as e:
            print(e)
            return None
        
    async def get_messenger(self, id:int): 
        pass
    
