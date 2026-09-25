from service_agent.core.models import Action
from service_agent.tools.gateway import ApprovalRequired
class Agent:
    name="agent"
    def __init__(self,gateway):self.gateway=gateway
    async def action(self,state,a:Action):
        try:
            r=await self.gateway.execute(a,set(state.get("roles",[])),state.get("approved",False))
            return {**state,"results":[*state.get("results",[]),r]}
        except ApprovalRequired as e:
            return {**state,"pending_action":e.action.model_dump(mode="json"),"answer":"Approval required before external mutation."}
