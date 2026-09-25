import asyncio,time
class IdempotencyStore:
 def __init__(self,ttl=86400):self.ttl=ttl;self.d={};self.lock=asyncio.Lock()
 async def reserve(self,key):
  async with self.lock:
   v=self.d.get(key)
   if v and time.time()-v["ts"]<self.ttl:return False,v.get("result")
   self.d[key]={"ts":time.time(),"result":None};return True,None
 async def commit(self,key,result):
  async with self.lock:self.d[key]={"ts":time.time(),"result":result}
