from models.request.login import LoginReq
from models.data.nsms import Login
from uuid import uuid1
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class LoginRepository:
    async def insert_login(self, login: LoginReq, db:AsyncSession) ->bool:
        login_l = Login(id=login.id,  username=login.username, password=login.password, user_type=login.user_type)
        try:
            db.add(login_l)
            await db.commit()
            await db.refresh(login_l)
        except Exception as e:
            print(e)
            await db.rollback()
            return False
        else:
            return True

    async def update_login(self, lreq: LoginReq, db:AsyncSession):
        login_l = Login(id=lreq.id,  username=lreq.username, password=lreq.password, user_type=lreq.user_type)
        try:
            result = await db.execute(select(Login).where(lreq.id == id))
            user = result.scalar_one_or_none()
            if user:
                for key, value in login_l.items():
                    setattr(user, key, value)
                await db.commit()
            else:
                print("User Not Found")
                return False
        except Exception as e:
            print(e)
            await db.rollback()
            return False
        else:
            return True

    async def delete_login(self, id:int, db: AsyncSession):
        try:
            result = await db.execute(select(Login).delete(Login.id == id))
            user = result.scalars().all()
            if user:
                db.delete(user)                                      
                db.commit()
                print(f" user id {id} deleted")
            else:
                print(f"Unable to find the user id {id} for Deletion")
            return True
        except Exception as e:
            print(e)
            await db.rollback()
            return False

    async def get_all_login(self, db: AsyncSession):
        try:
            result = await db.execute(select(Login))           
            users = result.scalars().all()
            print("Is there any exception")
            print(users)
            return users
        except Exception as e:
            print(e)
            print("You got an Exception")
            await db.rollback()
            return None
