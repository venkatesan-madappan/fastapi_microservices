import asyncio

my_list = [({'payable': 678.0, 'date_approved': '2025-08-10', 'received_by': 'whom', 'date_received': '2025-08-10', 'vendor_id': 1, 'admin_id': 1, 'approved_by': 'who', 'id': 1, 'date_billed': '2025-08-10', 'total_issues': 5}, {'lastname': 'Admin2', 'date_started': '2025-08-10', 'id': 1, 'age': 45, 'firstname': 'Admin2', 'status': 1, 'login_id': 1, 'birthday': '2025-08-10'}), \
           ({'payable': 890.0, 'date_approved': '2025-08-13', 'received_by': 'iam', 'date_received': '2025-08-13', 'vendor_id': 1, 'admin_id': 1, 'approved_by': 'Whom', 'id': 2, 'date_billed': '2025-08-13', 'total_issues': 2}, {'lastname': 'Admin2', 'date_started': '2025-08-10', 'id': 1, 'age': 45, 'firstname': 'Admin2', 'status': 1, 'login_id': 1, 'birthday': '2025-08-10'}), \
           ({'payable': 234.0, 'date_approved': '2025-08-13', 'received_by': 'iam3', 'date_received': '2025-08-13', 'vendor_id': 1, 'admin_id': 1, 'approved_by': 'Whom3', 'id': 3, 'date_billed': '2025-08-13', 'total_issues': 3}, {'lastname': 'Admin2', 'date_started': '2025-08-10', 'id': 1, 'age': 45, 'firstname': 'Admin2', 'status': 1, 'login_id': 1, 'birthday': '2025-08-10'}), \
           ({'payable': 567.0, 'date_approved': '2025-08-13', 'received_by': 'iam4', 'date_received': '2025-08-13', 'vendor_id': 1, 'admin_id': 1, 'approved_by': 'Whom4', 'id': 4, 'date_billed': '2025-08-13', 'total_issues': 4}, {'lastname': 'Admin2', 'date_started': '2025-08-10', 'id': 1, 'age': 45, 'firstname': 'Admin2', 'status': 1, 'login_id': 1, 'birthday': '2025-08-10'}), \
           ({'payable': 964.0, 'date_approved': '2025-08-13', 'received_by': 'iam5', 'date_received': '2025-08-13', 'vendor_id': 1, 'admin_id': 1, 'approved_by': 'Whom5', 'id': 5, 'date_billed': '2025-08-13', 'total_issues': 5}, {'lastname': 'Admin2', 'date_started': '2025-08-10', 'id': 1, 'age': 45, 'firstname': 'Admin2', 'status': 1, 'login_id': 1, 'birthday': '2025-08-10'}), \
            ({'payable': 4567.0, 'date_approved': '2025-08-13', 'received_by': 'iam6', 'date_received': '2025-08-13', 'vendor_id': 1, 'admin_id': 1, 'approved_by': 'Whom6', 'id': 6, 'date_billed': '2025-08-13', 'total_issues': 6}, {'lastname': 'Admin2', 'date_started': '2025-08-10', 'id': 1, 'age': 45, 'firstname': 'Admin2', 'status': 1, 'login_id': 1, 'birthday': '2025-08-10'}), \
                ({'payable': 4567.0, 'date_approved': '2025-08-13', 'received_by': 'iam7', 'date_received': '2025-08-13', 'vendor_id': 1, 'admin_id': 2, 'approved_by': 'Whom7', 'id': 7, 'date_billed': '2025-08-13', 'total_issues': 6}, {'lastname': 'Admin', 'date_started': '2025-08-13', 'id': 2, 'age': 11, 'firstname': 'Vendan', 'status': 1, 'login_id': 2, 'birthday': '2025-08-13'}), 
                ({'payable': 4567.0, 'date_approved': '2025-08-13', 'received_by': 'iam8', 'date_received': '2025-08-13', 'vendor_id': 1, 'admin_id': 2, 'approved_by': 'Whom8', 'id': 8, 'date_billed': '2025-08-13', 'total_issues': 6}, {'lastname': 'Admin', 'date_started': '2025-08-13', 'id': 2, 'age': 11, 'firstname': 'Vendan', 'status': 1, 'login_id': 2, 'birthday': '2025-08-13'})]

async def process_billing(query_list):
    billing_list = []
    async def extract_billing(qlist, q: asyncio.Queue):
        assigned_billing = {}
        for bill, adm in qlist:
            await asyncio.sleep(1)
            assigned_billing['admin_name'] = f" {adm['firstname']} {adm['lastname']}"
            assigned_billing['billing_items'] = bill
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
            for item in billing_items:
                billing_list.append({'admin_name': name, 'billing ': item})
            q.task_done()
        print(billing_list)
    q = asyncio.Queue()
    producer = asyncio.create_task(build_billing_sheet(q))
    consumer = asyncio.create_task(extract_billing(query_list, q))
    await asyncio.gather(producer, consumer)

if __name__ == "__main__":
    asyncio.run(process_billing(my_list))

