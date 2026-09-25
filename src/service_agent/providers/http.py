import httpx
from tenacity import retry,stop_after_attempt,wait_exponential_jitter,retry_if_exception_type
class Transient(Exception):pass
class ResilientHTTP:
 def __init__(self,timeout=15):self.c=httpx.AsyncClient(timeout=httpx.Timeout(timeout),follow_redirects=False)
 @retry(stop=stop_after_attempt(3),wait=wait_exponential_jitter(initial=.2,max=4),retry=retry_if_exception_type(Transient),reraise=True)
 async def request(self,method,url,**kw):
  r=await self.c.request(method,url,**kw)
  if r.status_code in (429,500,502,503,504):raise Transient(str(r.status_code))
  r.raise_for_status();return r
