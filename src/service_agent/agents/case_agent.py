from service_agent.agents.base import Agent
from service_agent.core.models import Action,Risk
class CaseAgent(Agent):
 name="case"
 async def run(self,s):
  if not s.get("case"):return s
  a=Action(agent=self.name,tool="case.update",args={"id":s["case"]["id"],"patch":{"status":"in_progress"}},
           risk=Risk.WRITE,reason="update service case")
  return await self.action(s,a)
