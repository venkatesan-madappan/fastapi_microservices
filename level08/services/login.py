import asyncio

async def build_user_list(user_records):
    user_list = []
    for record in user_records:
        await asyncio.sleep(1)
        user_list.append("".join([str(record.id), record.username, record.password]))
    return user_list

async def count_login(user_records):
    await asyncio.sleep(1)
    return len(user_records)
