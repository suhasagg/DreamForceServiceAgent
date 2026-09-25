from service_agent.agents.base import Agent
from service_agent.core.models import Action,Risk
class RefundAgentV2(Agent):
 name="refund"
 def __init__(self,g,idempotency,orders):super().__init__(g);self.ids=idempotency;self.orders=orders
 async def run(self,s):
  amount=float(s.get("refund_amount",0))
  if amount<=0:return {**s,"answer":"A positive refund amount is required.","handoff":True}
  if amount>500:return {**s,"answer":"Refund exceeds autonomous policy threshold; human review required.","handoff":True}
  key=f'{s["tenant_id"]}:{s["request_id"]}:refund'
  fresh,prior=await self.ids.reserve(key)
  if not fresh:return {**s,"results":[*s.get("results",[]),prior],"answer":"Existing refund result returned idempotently."}
  a=Action(agent=self.name,tool="refund.create",args={"customer_id":s["customer_id"],"amount":amount,"idempotency_key":key},
           risk=Risk.FINANCIAL,reason="validated customer refund")
  out=await self.action(s,a)
  if out.get("results"):await self.ids.commit(key,out["results"][-1])
  return out
