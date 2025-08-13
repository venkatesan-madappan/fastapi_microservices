from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.data.nsms import Admin, Login, Billing
from models.request.admin import AdminReq


class AdminRepository:
    async def insert_admin(self, req: AdminReq, db: AsyncSession):
        try:
            admin_l = Admin(id=req.id, firstname=req.firstname, lastname=req.lastname, \
                            age=req.age, date_started=req.date_started, status=req.status, \
                            login_id=req.login_id, birthday=req.birthday)
            db.add(admin_l)
            await db.commit()
            return True
        except Exception as e:
            print(e)
            db.rollback()
            return False

    async def update_admin(self, eq: AdminReq, db: AsyncSession):
        try:
            admin_l = Admin(id, req.id, firstname=req.firstname, lastname=req.lastname, \
                            age=req.age, date_started=req.date_started, status=req.status, \
                            login_id=req.login_id, birthday=req.birthday)
            result = await db.execute(select(Admin).where(id == admin_l.id))
            admin_user = result.scalar_one_or_none()
            if admin_user:
                for key, value in admin_user.items():
                    setattr(admin_user, key, value)
                await db.commit()
            else:
                print("Admin User Not Found")
                return False
            return True
        except Exception as e:
            print(e)
            db.rollback()
            return False
        
    async def delete_admin(self, req: AdminReq, db: AsyncSession):
        try:
            result = await db.execute(select(Admin).delete(Admin.id == id))
            admin_user = result.scalars().all()
            if admin_user:
                db.delete(admin_user)                                      
                db.commit()
                print(f" admin_user id {id} deleted")
            else:
                print(f"Unable to find the admin_user id {id} for Deletion")
            return True
        except Exception as e:
            print(e)
            await db.rollback()
            return False

    async def list_all_admin(self, db: AsyncSession):
        try:
            result = await db.execute(select(Admin))           
            admin_user = result.scalars().all()
            print("Is there any exception")
            print(admin_user)
            return admin_user
        except Exception as e:
            print(e)
            print("You got an Exception")
            await db.rollback()
            return None

class AdminLoginRepository:
    async def join_login_admin(self, db: AsyncSession):
        # query = await db.execute(
        #     select(Admin).options(selectinload(Admin.login_id)))
        stmt = select(Admin, Login).join(Login, Admin.login_id == Login.id)
        result = await db.execute(stmt)
        return result.all()
        # result = query.scalars().all()
        # print(query)
        # return result


class BillingAdminRepository:
    async def join_admin_billing(self, db: AsyncSession):
        stmt = select(Billing, Admin).join(Admin, Billing.admin_id == Admin.id)
        result = await db.execute(stmt)
        return result.all()
        