import json
from psycopg_pool import AsyncConnectionPool
class PostgresConversationStore:
 def __init__(self,dsn):self.pool=AsyncConnectionPool(dsn,open=False)
 async def open(self):
  await self.pool.open()
  async with self.pool.connection() as c:
   await c.execute("""create table if not exists service_memory(
    tenant_id text,user_id text,thread_id text,key text,value jsonb,provenance text,
    updated_at timestamptz default now(),primary key(tenant_id,user_id,thread_id,key))""")
 async def put(self,t,u,th,k,v,p):
  if not p:raise ValueError("provenance required")
  async with self.pool.connection() as c:
   await c.execute("""insert into service_memory values(%s,%s,%s,%s,%s,%s,now())
    on conflict(tenant_id,user_id,thread_id,key) do update set value=excluded.value,provenance=excluded.provenance,updated_at=now()""",
    (t,u,th,k,json.dumps(v),p))
 async def get(self,t,u,th,k):
  async with self.pool.connection() as c:
   cur=await c.execute("select value from service_memory where tenant_id=%s and user_id=%s and thread_id=%s and key=%s",(t,u,th,k))
   row=await cur.fetchone();return row[0] if row else None
