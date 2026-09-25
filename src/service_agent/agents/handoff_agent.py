from service_agent.agents.base import Agent
class HandoffAgent(Agent):
 name="handoff"
 async def run(self,s):
  summary={"intent":s.get("intent"),"customer":s.get("customer"),"retrieved":s.get("retrieved",[])[:3],
           "reason":"explicit request or automation confidence/policy boundary"}
  return {**s,"handoff":True,"answer":"Transferred to a human service representative.","handoff_context":summary}
