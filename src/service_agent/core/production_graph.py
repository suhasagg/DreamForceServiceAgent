from langgraph.graph import StateGraph,START,END
from langgraph.types import interrupt
from langgraph.checkpoint.memory import InMemorySaver
from service_agent.core.models import State
from service_agent.tools.gateway import ToolGateway
from service_agent.core.idempotency import IdempotencyStore
from service_agent.providers.demo import DemoCRM,DemoOrders,DemoKnowledge
from service_agent.rag.retriever import Retriever
from service_agent.agents.security_agent import SecurityAgent
from service_agent.agents.intent_agent_v2 import IntentAgentV2
from service_agent.agents.customer360_agent import Customer360Agent
from service_agent.agents.knowledge_agent import KnowledgeAgent
from service_agent.agents.order_agent import OrderAgent
from service_agent.agents.refund_agent_v2 import RefundAgentV2
from service_agent.agents.handoff_agent import HandoffAgent
from service_agent.agents.response_agent_v2 import ResponseAgentV2
from service_agent.agents.quality_agent_v2 import QualityAgentV2

def build_production_graph(llm=None,checkpointer=None):
 gateway=ToolGateway();crm=DemoCRM();orders=DemoOrders();kbp=DemoKnowledge();ids=IdempotencyStore()
 async def refund_tool(a):return {"refund_id":"refund-demo","status":"submitted","amount":a["amount"],"idempotency_key":a["idempotency_key"]}
 gateway.register("refund.create",refund_tool)
 sec=SecurityAgent(gateway);intent=IntentAgentV2(gateway,llm);c360=Customer360Agent(gateway,crm,orders)
 kb=KnowledgeAgent(gateway,Retriever(kbp));order=OrderAgent(gateway);refund=RefundAgentV2(gateway,ids,orders)
 handoff=HandoffAgent(gateway);resp=ResponseAgentV2(gateway,llm);quality=QualityAgentV2(gateway)
 async def blocked(s):return s
 async def approval(s):
  if not s.get("pending_action"):return s
  decision=interrupt({"kind":"approval","action":s["pending_action"]})
  return {**s,"approved":bool(decision)}
 async def resume_action(s):
  if not s.get("approved"):return {**s,"answer":"Action denied.","pending_action":None}
  # Real production implementation reconstructs validated Action and executes once with signed approval context.
  return {**s,"answer":"Approval recorded; action is eligible for idempotent execution.","pending_action":None}
 def secroute(s):return "blocked" if s.get("security_flags") else "intent"
 def route(s):return {"refund":"refund","order":"order","human":"handoff"}.get(s.get("intent"),"knowledge")
 def post_refund(s):return "approval" if s.get("pending_action") else "quality"
 g=StateGraph(State)
 nodes={"security":sec.run,"blocked":blocked,"intent":intent.run,"customer360":c360.run,"knowledge":kb.run,
 "order":order.run,"refund":refund.run,"handoff":handoff.run,"response":resp.run,"quality":quality.run,
 "approval":approval,"resume_action":resume_action}
 for n,f in nodes.items():g.add_node(n,f)
 g.add_edge(START,"security");g.add_conditional_edges("security",secroute,{"blocked":"blocked","intent":"intent"});g.add_edge("blocked",END)
 g.add_edge("intent","customer360");g.add_conditional_edges("customer360",route,{"refund":"refund","order":"order","handoff":"handoff","knowledge":"knowledge"})
 g.add_edge("knowledge","response");g.add_edge("response","quality");g.add_edge("order","quality");g.add_edge("handoff","quality")
 g.add_conditional_edges("refund",post_refund,{"approval":"approval","quality":"quality"});g.add_edge("approval","resume_action");g.add_edge("resume_action","quality");g.add_edge("quality",END)
 return g.compile(checkpointer=checkpointer or InMemorySaver())
