from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.request.billing import BillingReq
from models.data.nsms import Billing, Vendor

class BillingRepository:
    async def billing_insert(self, req:BillingReq, db:AsyncSession) -> bool:
        billing_l = Billing(id= req.id, payable=req.payable, approved_by=req.approved_by, \
                            date_approved=req.date_approved, date_billed=req.date_billed, \
                                received_by=req.received_by, date_received=req.date_received, \
                                    total_issues=req.total_issues, \
                                    vendor_id=req.vendor_id, admin_id=req.admin_id)
                                    
        try:
            db.add(billing_l)
            await db.commit()
            return True
        except Exception as e:
            print(e)
            await db.rollback()
            return False

    async def get_all_billing(self, db: AsyncSession):
        try:
            result = await db.execute(select(Billing))           
            bill_result = result.scalars().all()
            print("Is there any exception")
            print(bill_result)
            return bill_result
        except Exception as e:
            print(e)
            print("You got an Exception")
            await db.rollback()
            return None

class BillingAdminRepository:
    async def join_billing_admin(self, ):
        pass

class BillingVendorRepository:
    async def join_billing_vendor(self, bill_date, db=AsyncSession):
        stmt = (select(Vendor, Billing).join(Billing, Billing.id == Vendor.id).where(Billing.date_billed == bill_date))
        # query_result = await db.query(Vendor, Billing).join(Billing.date_billed == bill_date).all()
        # billing_vendors = query_result.scalar().all()
        billing_vendors = await db.execute(stmt)
        return billing_vendors.all()


# class BillingReq(BaseModel):
#     id: int
#     payable: float
#     approved_by: str
#     date_approved: date
#     date_billed: date
#     received_by: str
#     date_received: date
#     total_issues: int
#     vendor_id: int
#     admin_id: int