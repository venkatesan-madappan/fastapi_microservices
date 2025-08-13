import asyncio
from asyncio import Queue
from models.data.nsms import Admin, Billing
from fastapi.encoders import jsonable_encoder
# from cryptography.fernet import Fernet

async def process_billing(query_list):
    billing_list = []
    async def extract_billing(qlist, q: asyncio.Queue):
        assigned_billing = {}
        for bill, adm in qlist:
            await asyncio.sleep(1)
            assigned_billing['admin_name'] = f" {adm.firstname} {adm.lastname}"
            assigned_billing['billing_items'] = jsonable_encoder(bill)
            print("Placing it in Q ")
            await q.put(assigned_billing)
        await q.put(None)
    
    async def build_billing_sheet(q: asyncio.Queue):
        while True:
            await asyncio.sleep(1)
            assigned_billing = await q.get()
            if assigned_billing is None:
                break  # exit signal
            print("Taken from Q")
            name = assigned_billing['admin_name']
            billing_items = assigned_billing['billing_items']
            # for item in billing_items:
            billing_list.append({'admin_name': name, 'billing ': billing_items})
            q.task_done()
        # print(billing_list)
    q = asyncio.Queue()
    producer = asyncio.create_task(build_billing_sheet(q))
    consumer = asyncio.create_task(extract_billing(query_list, q))
    await asyncio.gather(producer, consumer)
    return billing_list
 
async def extract_profile(admin_details):
    profile = {}
    login = admin_details.parent
    profile['firstname'] = admin_details.firstname
    profile['lastname'] = admin_details.lastname
    profile['age'] = admin_details.age 
    profile['status'] = admin_details.status 
    profile['birthday'] = admin_details.birthday 
    profile['username'] = login.username 
    profile['password'] = login.password 
    await asyncio.sleep(1)
    return profile

async def extract_condensed(profiles):
    profile_info = " ".join([profiles['firstname'], profiles['lastname'], profiles['username'], profiles['password']])
    await asyncio.sleep(1)
    return profile_info 

async def decrypt_profile(profile_info):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encoded_profile = fernet.encrypt(profile_info.encode())
    return encoded_profile

async def extract_enc_admin_profile(admin_rec):
    p = await extract_profile(admin_rec)
    pinfo = await extract_condensed(p)
    encp = await decrypt_profile(pinfo)
    return encp