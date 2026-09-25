from service_agent.agents.base import Agent
class ResponseAgent(Agent):
 name="response"
 async def run(self,s):
  if s.get("answer"):return s
  docs=s.get("retrieved",[])
  answer=docs[0]["text"] if docs else "I could not find a grounded answer; I will route this for human review."
  return {**s,"answer":answer,"handoff":not bool(docs)}
