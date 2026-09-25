from service_agent.agents.base import Agent
class QualityAgent(Agent):
 name="quality"
 async def run(self,s):
  grounded=bool(s.get("retrieved")) or s.get("intent") in ("order","human")
  return {**s,"metrics":{**s.get("metrics",{}),"grounded":grounded,"result_count":len(s.get("results",[]))}}
