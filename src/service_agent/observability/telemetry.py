import time,structlog
log=structlog.get_logger()
class span:
 def __init__(self,name,**attrs):self.name=name;self.attrs=attrs
 def __enter__(self):self.t=time.perf_counter();log.info("span.start",name=self.name,**self.attrs);return self
 def __exit__(self,*a):log.info("span.end",name=self.name,duration_ms=(time.perf_counter()-self.t)*1000,**self.attrs)
