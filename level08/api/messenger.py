
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from kafka import KafkaProducer, KafkaConsumer

from sse_starlette.sse import EventSourceResponse

import json
import asyncio
from datetime import date, datetime
from uuid import uuid4

from models.request.messenger import MessengerReq
from models.data.nsms import Messenger, Vendor
from repository.messenger import MessengerRepository
from config.db.db_setup import get_async_session

SSE_STREAM_DELAY = 1  # second
SSE_RETRY_TIMEOUT = 15000  # milisecond


producer = KafkaProducer(bootstrap_servers='localhost:9092')
consumer = KafkaConsumer('newstopic')

router = APIRouter()

def json_date_serializer(obj):
     if isinstance(obj, (datetime, date)):
          return obj.isoformat()
     raise TypeError("Data is not serializable" %type(obj))
     
def date_hook_deserializer(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.strptime(value, "%Y= %m-%d").date()
        except:
            pass
    return json_dict

@router.post("/messenger/add")
async def add_messenger(req: MessengerReq, db: AsyncSession = Depends(get_async_session)):
    repo = MessengerRepository()
    result = await repo.insert_messenger(req=req, db=db)
    if result == True: 
        return req 
    else: 
        return JSONResponse(content={'message':'update Messenger profile problem encountered'}, status_code=500)

#TO-DO
@router.post("/messenger/kafka/send")
async def send_messnger_details(req: MessengerReq): 
    # print(MessengerReq)
    messenger_dict = req.dict(exclude_unset=True)
    print(messenger_dict)
    producer.send("newstopic", bytes(str(json.dumps(messenger_dict, default=json_date_serializer)), 'utf-8'))
    return {"message":"Messenger details sent"}

#TO-DO
@router.get("/messenger/sse/add")
async def send_message_stream(req: Request):
    async def event_provider():
        while True:
            if await req.is_disconnected():
                break
            print("Before Consumer Poll")
            message = consumer.poll()
            print("After Consumer Poll")
            if not len(message.items()) == 0:
                print("Message is not zero")                        
                for tp, records in message.items():
                    print("Before record processing")                        
                    for rec in records:
                        print("Inside Records")                        
                        messenger_dict = json.loads(rec.value.decode('utf-8'), object_hook=date_hook_deserializer )
                                             
                        repo = MessengerRepository()
                        result = None
                        with get_async_session() as db:
                            result = await repo.insert_messenger(req=messenger_dict, db=db)
                        id = uuid4()
                        yield {
                            "event": "Added messenger status: {}, Received: {}". format(result, datetime.utcfromtimestamp(rec.timestamp // 1000).strftime("%B %d, %Y [%I:%M:%S %p]")),
                            "id": str(id),
                            "retry": SSE_RETRY_TIMEOUT,
                            "data": rec.value.decode('utf-8')
                        }
            print("Befor SSE Stream Delay")                        
            await asyncio.sleep(SSE_STREAM_DELAY)
    return EventSourceResponse(event_provider())




