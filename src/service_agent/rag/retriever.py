class Retriever:
    def __init__(self,provider):self.provider=provider
    async def retrieve(self,query,tenant,k=5):
        docs=await self.provider.search(query,tenant,k)
        # Tenant filter is defense-in-depth even if backend already scopes.
        return [d for d in docs if d.get("tenant_id")==tenant][:k]
