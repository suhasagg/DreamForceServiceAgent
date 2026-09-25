class DemoCRM:
 async def customer(self,id):return {"id":id,"name":"Demo Customer","tier":"gold"}
 async def update_case(self,id,patch):return {"id":id,**patch}
class DemoOrders:
 async def list_orders(self,customer_id):return [{"id":"ord-1","status":"delivered","customer_id":customer_id}]
 async def order(self,id):return {"id":id,"status":"delivered"}
class DemoKnowledge:
 async def search(self,query,tenant_id,k=5):
  return [{"id":"kb-1","title":"Returns policy","text":"Eligible items may be returned according to policy.","score":.91,"tenant_id":tenant_id}]
class DemoMessaging:
 async def send(self,channel,target,body):return {"status":"dry-run","channel":channel,"target":target}
