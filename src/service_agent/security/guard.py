import re
class InputGuard:
    patterns=[r"ignore .*instructions",r"reveal .*system prompt",r"(api|secret)[-_ ]?key",r"disable .*security"]
    def inspect(self,text):
        return [p for p in self.patterns if re.search(p,text,re.I)]
def redact(text:str)->str:
    text=re.sub(r'[\w.+-]+@[\w-]+\.[\w.-]+','[EMAIL]',text)
    text=re.sub(r'\b(?:\d[ -]*?){13,19}\b','[PAYMENT_DATA]',text)
    return text
