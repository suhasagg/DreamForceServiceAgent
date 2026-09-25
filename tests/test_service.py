import pytest
from service_agent.core.graph import graph
@pytest.mark.asyncio
async def test_grounded_knowledge():
 s=await graph.ainvoke({"request_id":"1","tenant_id":"t","user_id":"u","customer_id":"c","message":"return policy",
 "roles":[],"approved":False,"results":[],"retrieved":[],"security_flags":[],"metrics":{}})
 assert s["retrieved"] and s["metrics"]["grounded"]
@pytest.mark.asyncio
async def test_refund_policy_denies_without_role():
 s=await graph.ainvoke({"request_id":"2","tenant_id":"t","user_id":"u","customer_id":"c","message":"refund my order",
 "roles":[],"approved":False,"refund_amount":20,"results":[],"retrieved":[],"security_flags":[],"metrics":{}})
 assert not s["results"][0]["ok"]
