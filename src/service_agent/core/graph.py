from langgraph.graph import StateGraph,START,END
from service_agent.core.models import State
from service_agent.tools.gateway import ToolGateway
from service_agent.providers.demo import DemoCRM,DemoOrders,DemoKnowledge,DemoMessaging
from service_agent.rag.retriever import Retriever
from service_agent.agents.security_agent import SecurityAgent
from service_agent.agents.intent_agent import IntentAgent
from service_agent.agents.customer360_agent import Customer360Agent
from service_agent.agents.knowledge_agent import KnowledgeAgent
from service_agent.agents.order_agent import OrderAgent
from service_agent.agents.refund_agent import RefundAgent
from service_agent.agents.handoff_agent import HandoffAgent
from service_agent.agents.response_agent import ResponseAgent
from service_agent.agents.quality_agent import QualityAgent
gway=ToolGateway();crm=DemoCRM();orders=DemoOrders();knowledge=DemoKnowledge()
async def refund(a):return {"status":"dry-run","refund_id":"ref-demo","amount":a.get("amount")}
async def case_update(a):return await crm.update_case(a["id"],a["patch"])
gway.register("refund.create",refund);gway.register("case.update",case_update)
sec=SecurityAgent(gway);intent=IntentAgent(gway);c360=Customer360Agent(gway,crm,orders)
kb=KnowledgeAgent(gway,Retriever(knowledge));order=OrderAgent(gway);refund_agent=RefundAgent(gway)
handoff=HandoffAgent(gway);response=ResponseAgent(gway);quality=QualityAgent(gway)
def after_sec(s):return "blocked" if s.get("security_flags") else "intent"
def route(s):
 return {"refund":"refund","order":"order","human":"handoff"}.get(s.get("intent"),"knowledge")
async def blocked(s):return s
def build():
 g=StateGraph(State)
 for n,f in {"security":sec.run,"blocked":blocked,"intent":intent.run,"customer360":c360.run,"knowledge":kb.run,
             "order":order.run,"refund":refund_agent.run,"handoff":handoff.run,"response":response.run,"quality":quality.run}.items():g.add_node(n,f)
 g.add_edge(START,"security");g.add_conditional_edges("security",after_sec,{"blocked":"blocked","intent":"intent"});g.add_edge("blocked",END)
 g.add_edge("intent","customer360");g.add_conditional_edges("customer360",route,{"refund":"refund","order":"order","handoff":"handoff","knowledge":"knowledge"})
 g.add_edge("knowledge","response");g.add_edge("order","quality");g.add_edge("refund","quality");g.add_edge("handoff","quality")
 g.add_edge("response","quality");g.add_edge("quality",END);return g.compile()
graph=build()
