from dataclasses import dataclass
from service_agent.core.models import Action,Risk
@dataclass(frozen=True)
class Decision: allow:bool; approval:bool; reason:str
class PolicyEngine:
    deny={"shell","raw_sql","credential.read","admin.impersonate"}
    approval={Risk.WRITE,Risk.COMMUNICATE,Risk.FINANCIAL,Risk.PRIVILEGED}
    def decide(self,a:Action,roles:set[str]=set())->Decision:
        if a.tool in self.deny:return Decision(False,False,"globally denied capability")
        if a.risk==Risk.FINANCIAL and "refund_operator" not in roles:return Decision(False,False,"refund role required")
        return Decision(True,a.risk in self.approval,"approved by policy" if a.risk==Risk.READ else "human approval required")
