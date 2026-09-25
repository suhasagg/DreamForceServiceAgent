from service_agent.agents.base import Agent
class OrderAgent(Agent):
 name="order"
 async def run(self,s):
  orders=s.get("customer",{}).get("orders",[])
  return {**s,"answer":f"I found {len(orders)} order(s). "+(f"Latest status: {orders[0]['status']}." if orders else "")}
