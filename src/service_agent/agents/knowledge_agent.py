from service_agent.agents.base import Agent
class KnowledgeAgent(Agent):
 name="knowledge"
 def __init__(self,g,retriever):super().__init__(g);self.r=retriever
 async def run(self,s):
  docs=await self.r.retrieve(s["message"],s["tenant_id"])
  return {**s,"retrieved":docs}
