import pytest
from service_agent.core.production_graph import build_production_graph
@pytest.mark.asyncio
async def test_grounded_v2():
 g=build_production_graph()
 s=await g.ainvoke({"request_id":"r","tenant_id":"t","user_id":"u","customer_id":"c","message":"return policy",
 "roles":[],"approved":False,"results":[],"retrieved":[],"security_flags":[],"metrics":{}},
 config={"configurable":{"thread_id":"t1"}})
 assert s.get("citations")==["kb-1"] and s["metrics"]["citation_valid"]
