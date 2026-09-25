from service_agent.core.models import Action
from service_agent.security.policy import PolicyEngine
from service_agent.security.audit import Audit
class ApprovalRequired(Exception):
    def __init__(self,a):self.action=a
class ToolGateway:
    def __init__(self):self.policy=PolicyEngine();self.audit=Audit();self.handlers={}
    def register(self,n,h):self.handlers[n]=h
    async def execute(self,a:Action,roles=set(),approved=False):
        d=self.policy.decide(a,roles);self.audit.write({"kind":"policy","action":a.model_dump(mode="json"),"decision":d.__dict__})
        if not d.allow:return {"ok":False,"error":d.reason}
        if d.approval and not approved:raise ApprovalRequired(a)
        if a.tool not in self.handlers:return {"ok":False,"error":"tool unavailable"}
        try:r=await self.handlers[a.tool](a.args);out={"ok":True,"output":r}
        except Exception as e:out={"ok":False,"error":type(e).__name__}
        self.audit.write({"kind":"result","action_id":a.id,"result":out});return out
