def _C (c:str) -> str:
    import subprocess
    from shlex import split
    result = subprocess.run(split(c) , stdout=subprocess.PIPE)
    return result.stdout.decode()

import time

class cache :
    def __init__ (self,func,refresh:int=40,args=[],wargs={}):
        self.refresh = refresh
        self.func = func
        self._last_check = 0
        self.args = args
        self.wargs = wargs
        self.response = None
        self.renew()
    
    def __call__ (self):
        if time.time() - self._last_check >= self.refresh :
            self.renew()
        return self.response

    def renew(self):
        from threading import Thread
        def _renew():
            self.response = self.func(*self.args,**self.wargs)
            self._last_check = time.time()
        Thread(target=_renew).start()