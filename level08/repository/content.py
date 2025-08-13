from models.data.nsms import Content, Publication
from models.request.content import ContentReq
from datetime import date, time
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

class ContentRepository: 
    
    async def insert_content(self, req = ContentReq, db=AsyncSession) -> bool: 
        content_l = Content(id = req.id, publication_id = req.publication_id, \
                            headline = req.headline,content = req.content,\
                                content_type = req.content_type, \
                                    date_published = req.date_published)
        try:
            db.add(content_l)
            await db.commit()
            return True
        except Exception as e: 
            print(e)
            await db.rollback()
            return False 
    
    async def update_content(self, id:int) -> bool: 
       pass
   
    async def delete_content(self, id:int) -> bool: 
        pass
    
    async def get_all_content(self):
        pass
        
    async def get_content(self, id:int): 
        pass
    

