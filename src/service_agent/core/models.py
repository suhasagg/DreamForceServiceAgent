from __future__ import annotations
from enum import Enum
from typing import Any, TypedDict
from pydantic import BaseModel,Field
from uuid import uuid4
class Risk(str,Enum): READ="read"; WRITE="write"; COMMUNICATE="communicate"; FINANCIAL="financial"; PRIVILEGED="privileged"
class Principal(BaseModel):
    tenant_id:str; user_id:str; roles:set[str]=Field(default_factory=set)
class Customer(BaseModel):
    id:str; name:str|None=None; email:str|None=None; tier:str|None=None; attributes:dict[str,Any]=Field(default_factory=dict)
class Case(BaseModel):
    id:str=Field(default_factory=lambda:str(uuid4())); customer_id:str; subject:str; description:str
    status:str="open"; priority:str="normal"; channel:str="web"; metadata:dict[str,Any]=Field(default_factory=dict)
class Action(BaseModel):
    id:str=Field(default_factory=lambda:str(uuid4())); agent:str; tool:str; args:dict[str,Any]=Field(default_factory=dict)
    risk:Risk=Risk.READ; reason:str=""
class State(TypedDict,total=False):
    request_id:str; tenant_id:str; user_id:str; message:str; intent:str; customer:dict; case:dict
    retrieved:list[dict]; plan:list[dict]; pending_action:dict|None; approved:bool
    results:list[dict]; security_flags:list[str]; handoff:bool; answer:str; metrics:dict
