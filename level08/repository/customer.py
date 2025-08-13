from models.data.nsms import Customer, Login
from models.request.customer import CustomerReq
from sqlalchemy.ext.asyncio import AsyncSession

class CustomerRepository: 
    
    async def insert_customer(self, req:CustomerReq, db: AsyncSession) -> bool: 
        customer_l = Customer(id  = req.id, firstname = req.firstname, lastname = req.lastname, \
                              age = req.age, birthday = req.birthday, date_subscribed = req.date_subscribed, \
                              status = req.status, subscription_type = req.subscription_type, \
                              login_id = req.login_id)
        try:
            db.add(customer_l)
            await db.commit()
            return True
        except Exception as e: 
            print(e)
            db.rollback()
            return False 
    
    async def get_all_customer(self):
        return await Customer.query.gino.all()
        
    async def get_customer(self, id:int): 
        return await Customer.get(id)
    

