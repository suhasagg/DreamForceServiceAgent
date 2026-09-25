from service_agent.agents.base import Agent
from service_agent.security.guard import InputGuard
class SecurityAgent(Agent):
 name="security"
 def __init__(self,g):super().__init__(g);self.guard=InputGuard()
 async def run(self,s):
  flags=self.guard.inspect(s.get("message",""));return {**s,"security_flags":flags,"answer":"Request blocked." if flags else s.get("answer","")}
