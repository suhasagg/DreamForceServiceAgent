from service_agent.agents.base import Agent
class QualityAgentV2(Agent):
 name="quality"
 async def run(self,s):
  citations=s.get("citations",[]);docs={d["id"] for d in s.get("retrieved",[])}
  citation_valid=all(c in docs for c in citations)
  return {**s,"metrics":{**s.get("metrics",{}),"citation_valid":citation_valid,
   "grounded":bool(citations) or s.get("intent") in ("order","human"),
   "handoff":bool(s.get("handoff")),"tool_failures":sum(not r.get("ok",False) for r in s.get("results",[]))}}
