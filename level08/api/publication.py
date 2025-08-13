from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from models.request.publication import PublicationReq
from models.data.nsms import Publication, Messenger
from repository.publication import PublicationRepository
from config.db.db_setup import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter()

@router.post("/publication/add")
async def add_publication(req: PublicationReq, db: AsyncSession = Depends(get_async_session)):
    repo = PublicationRepository()
    result = await repo.insert_publication(req=req, db=db)
    if result == True: 
        return req 
    else: 
        return JSONResponse(content={'message':'update trainer profile problem encountered'}, status_code=500)
    
@router.get("/publication/list")
async def list_publication(db:AsyncSession = Depends(get_async_session)):
    repo = PublicationRepository()
    result = await repo.get_all_publication(db=db)
    if result:
        return result
    else:
        return JSONResponse(content={'message':'Publication List problem encountered'}, status_code=500)
