from pydantic import BaseModel,Field
from uuid import uuid4
class RequestContext(BaseModel):
 request_id:str=Field(default_factory=lambda:str(uuid4()))
 thread_id:str=Field(default_factory=lambda:str(uuid4()))
 tenant_id:str;user_id:str;roles:set[str]=Field(default_factory=set)
 idempotency_key:str=Field(default_factory=lambda:str(uuid4()))
 deadline_ms:int=30000
