from fastapi import FastAPI

from api import admin, login, billing, vendor, customer, publication, messenger, sales, subscription, content

from core import lifespan


app = FastAPI(lifespan=lifespan.lifespan)

app.include_router(login.router, prefix='/level08')
app.include_router(admin.router, prefix='/level08')
app.include_router(vendor.router, prefix='/level08')
app.include_router(customer.router, prefix='/level08')
app.include_router(billing.router, prefix='/level08')
app.include_router(messenger.router, prefix='/level08')
app.include_router(publication.router, prefix='/level08')
app.include_router(content.router, prefix='/level08')
app.include_router(sales.router, prefix='/level08')
app.include_router(subscription.router, prefix='/level08')

