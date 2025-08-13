from models.data.nsms import Sales, Publication
from datetime import date, time
from models.data.nsms import Sales
from models.request.sales import SalesReq
from fastapi import Depends
from config.db.db_setup import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class SalesRepository: 
    
    async def insert_sales(self, req:SalesReq, db=AsyncSession) -> bool: 
        sales_l = Sales(publication_id = req.publication_id,copies_issued = req.copies_issued, \
                        copies_sold = req.copies_sold,date_issued = req.date_issued, \
                            revenue = req.revenue, profit = req.profit)
        try:
            db.add(sales_l)
            await db.commit()
            return True
        except Exception as e: 
            print(e)
            await db.rollback()
            return False 
    
    async def update_sales(self, id:int) -> bool: 
       pass
   
    async def delete_sales(self, id:int) -> bool: 
        pass
    
    async def get_all_sales(self, db:AsyncSession):
        try:
            print(f"Lets see the type of DB : {type(db)}")
            result = await db.execute(select(Sales))           
            sales_l = result.scalars().all()
            print("Is there any exception")
            print(sales_l)
            return sales_l
        except Exception as e:
            print(e)
            print("You got an Exception")
            await db.rollback()
            return None

    async def get_sales(self, id:int): 
        pass
    

    
    
