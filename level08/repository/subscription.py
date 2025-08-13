from models.data.nsms import Subscription, Customer
from datetime import date, time
from typing import List, Dict, Any

from models.request.subscription import SubscriptionReq
from config.db.db_setup import create_async_engine

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class SubscriptionRepository: 
    
    async def insert_subscription(self, req:SubscriptionReq, db: AsyncSession)-> bool: 
        sub_l = Subscription(id = req.id, customer_id = req.customer_id, branch = req.branch, \
                             price = req.price, qty = req.qty, date_purchased = req.date_purchased)            
        try:
            db.add(sub_l)
            await db.commit()
            return True
        except Exception as e: 
            print(e)
            await db.rollback()
            return False 
    
    async def update_subscription(self, id:int, details:Dict[str, Any]) -> bool: 
       pass
   
    async def delete_subscription(self, id:int) -> bool: 
        pass
    
    async def get_all_subscription(self):
        pass
        
    async def get_subscription(self, id:int): 
        pass
    



