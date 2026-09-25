import math,re
class HybridRetriever:
 """Production interface with deterministic local BM25-ish fallback; replace vector_search callback with pgvector/OpenSearch."""
 def __init__(self,documents,vector_search=None):self.docs=documents;self.vector_search=vector_search
 def lexical(self,q,tenant,k=10):
  qt=set(re.findall(r"\w+",q.lower()));scored=[]
  for d in self.docs:
   if d.get("tenant_id")!=tenant:continue
   dt=set(re.findall(r"\w+",d["text"].lower()));score=len(qt&dt)/(len(qt|dt) or 1)
   if score:scored.append((score,d))
  return [dict(d,lexical_score=s) for s,d in sorted(scored,key=lambda x:x[0],reverse=True)[:k]]
 async def search(self,q,tenant,k=5):
  lex=self.lexical(q,tenant,k*2);vec=await self.vector_search(q,tenant,k*2) if self.vector_search else []
  merged={}
  for rank,d in enumerate(lex):merged[d["id"]]=merged.get(d["id"],0)+1/(60+rank)
  for rank,d in enumerate(vec):merged[d["id"]]=merged.get(d["id"],0)+1/(60+rank)
  by={d["id"]:d for d in lex+vec}
  return [dict(by[i],rrf_score=s) for i,s in sorted(merged.items(),key=lambda x:x[1],reverse=True)[:k]]
