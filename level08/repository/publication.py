from models.data.nsms import Publication, Vendor, Messenger
from models.request.publication import PublicationReq
from datetime import date, time
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class PublicationRepository: 
    
    async def insert_publication(self, req:PublicationReq, db:AsyncSession) -> bool: 
        pub_l = Publication(id = req.id, name = req.name, type = req.type, \
                    vendor_id = req.vendor_id, messenger_id = req.messenger_id)
        try:
            db.add(pub_l)
            await db.commit()
            return True
        except Exception as e: 
            print(e)
            return False 
    
    async def update_publication(self, id:int, details:Dict[str, Any]) -> bool: 
        pass
   
    async def delete_publication(self, id:int) -> bool: 
        pass
    
    async def get_all_publication(self, db=AsyncSession):
        try:
            result = await db.execute(select(Publication))
            publication_l = result.scalars().all()
            return publication_l
        except Exception as e:
            print(e)
            await db.rollback()
            return None

        return await Publication.query.gino.all()
        
    async def get_publication(self, id:int): 
        return await Publication.get(id)
    

    
