import hashlib,json,time
class Audit:
    def __init__(self):self.events=[];self.prev="GENESIS"
    def write(self,event):
        b={"ts":time.time(),"prev":self.prev,**event}; raw=json.dumps(b,sort_keys=True,default=str).encode()
        b["hash"]=hashlib.sha256(raw).hexdigest();self.prev=b["hash"];self.events.append(b);return b["hash"]
