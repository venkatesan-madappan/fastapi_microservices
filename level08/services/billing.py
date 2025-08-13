import asyncio
import os
from celery import Celery

async def generate_billing_sheet(billing_date, billing_data):
    filepath = os.getcwd() + '/data/billing'+str(billing_date)+'.csv'
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, mode="a") as sheet:
        for record in billing_data:
            vendor = record[0]
            entry = ";".join([vendor.rep_firstname, vendor.rep_lastname, str(vendor.rep_id), str(vendor.date_consigned)])
            sheet.write(entry)
            await asyncio.sleep

# https://www.youtube.com/watch?v=9L77QExPmI0
#https://www.youtube.com/watch?v=VRHVEporra0
async def create_total_payables_year(billing_date, billing_data):
    pass

