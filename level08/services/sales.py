import asyncio
import rx
from rx.disposable import Disposable
from sqlalchemy.ext.asyncio import AsyncSession
from config.db.db_setup import get_async_session
from fastapi import Depends
from repository.sales import SalesRepository

async def process_list(observer, db:AsyncSession=Depends(get_async_session)):
    print("Inside Process list")
    repo = SalesRepository()
    print("Before get async session")
    print(f"Are we gettomg a Session Here")
    result = await repo.get_all_sales(db=db)
    print(f"Result is {result}")
    for item in result:
        record = " ".join([str(item.publication_id)])
        print(f" Record is : {record}")
        cost = item.copies_issued * 5.0
        projected_profit = cost - item.revenue
        diff_err = projected_profit - item.profit
        if(diff_err <= 0):
            observer.on_next(record)
        else:
            observer.on_error(record)
    observer.on_completed()

def create_observable(loop):
    def evaluate_profit(observer, scheduler):
        print("Going to create the future task")
        task = asyncio.ensure_future(process_list(observer), loop=loop)
        print("Out of future task")
        return Disposable(lambda: task.cancel())
    print("Going to create the Rx")
    return rx.create(evaluate_profit)

