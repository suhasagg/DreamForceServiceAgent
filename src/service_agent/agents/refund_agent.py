from service_agent.agents.base import Agent
from service_agent.core.models import Action,Risk
class RefundAgent(Agent):
 name="refund"
 async def run(self,s):
  a=Action(agent=self.name,tool="refund.create",args={"customer_id":s.get("customer_id"),"amount":s.get("refund_amount",0)},
           risk=Risk.FINANCIAL,reason="customer refund")
  return await self.action(s,a)
