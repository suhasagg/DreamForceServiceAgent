from service_agent.agents.base import Agent
class IntentAgent(Agent):
 name="intent"
 async def run(self,s):
  t=s.get("message","").lower()
  if any(x in t for x in ["refund","money back"]):i="refund"
  elif any(x in t for x in ["order","delivery","shipment"]):i="order"
  elif any(x in t for x in ["return","replace"]):i="return"
  elif any(x in t for x in ["agent","human","representative"]):i="human"
  else:i="knowledge"
  return {**s,"intent":i}
