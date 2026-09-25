from service_agent.agents.base import Agent
class Customer360Agent(Agent):
 name="customer360"
 def __init__(self,g,crm,orders):super().__init__(g);self.crm=crm;self.orders=orders
 async def run(self,s):
  cid=s.get("customer_id","customer-demo");c=await self.crm.customer(cid);o=await self.orders.list_orders(cid)
  return {**s,"customer":{**c,"orders":o}}
