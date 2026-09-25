import os
from service_agent.providers.http import ResilientHTTP
class SalesforceREST:
 """Real Salesforce REST adapter using a pre-obtained OAuth access token and instance URL."""
 def __init__(self,instance_url=None,access_token=None,http=None):
  self.base=(instance_url or os.environ["SALESFORCE_INSTANCE_URL"]).rstrip("/")
  self.token=access_token or os.environ["SALESFORCE_ACCESS_TOKEN"];self.http=http or ResilientHTTP()
 @property
 def h(self):return {"Authorization":f"Bearer {self.token}","Content-Type":"application/json"}
 async def query(self,soql):
  r=await self.http.request("GET",f"{self.base}/services/data/v66.0/query",headers=self.h,params={"q":soql});return r.json()
 async def get_contact(self,contact_id):
  r=await self.http.request("GET",f"{self.base}/services/data/v66.0/sobjects/Contact/{contact_id}",
    headers=self.h,params={"fields":"Id,Name,Email,AccountId"});return r.json()
 async def update_case(self,case_id,patch):
  await self.http.request("PATCH",f"{self.base}/services/data/v66.0/sobjects/Case/{case_id}",headers=self.h,json=patch)
  return {"id":case_id,**patch}
 async def create_case(self,payload):
  r=await self.http.request("POST",f"{self.base}/services/data/v66.0/sobjects/Case",headers=self.h,json=payload);return r.json()
