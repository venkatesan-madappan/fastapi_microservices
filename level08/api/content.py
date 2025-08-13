from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from models.request.content import ContentReq
from models.data.nsms import Content, Publication
from repository.content import ContentRepository
from config.db.db_setup import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.post("/content/add")
async def add_content(req: ContentReq, db:AsyncSession=Depends(get_async_session)):
    repo = ContentRepository()
    result = await repo.insert_content(req=req, db=db)
    if result == True: 
        return req 
    else: 
        return JSONResponse(content={'message':'update trainer profile problem encountered'}, status_code=500)
    
@router.get("/content/list")
async def list_content():
    repo = ContentRepository()
    result = await repo.get_all_content()
    return result