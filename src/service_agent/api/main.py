from uuid import uuid4
from fastapi import FastAPI
from pydantic import BaseModel
from service_agent.core.graph import graph
app=FastAPI(title="Enterprise Service Agent",version="1.0")
class Req(BaseModel):
 tenant_id:str="demo";user_id:str="user";customer_id:str="customer-demo";message:str
 roles:list[str]=[];approved:bool=False;refund_amount:float=0
@app.get("/health")
async def health():return {"ok":True}
@app.post("/v1/service")
async def service(r:Req):
 s={"request_id":str(uuid4()),**r.model_dump(),"results":[],"retrieved":[],"security_flags":[],"metrics":{}}
 return await graph.ainvoke(s)
