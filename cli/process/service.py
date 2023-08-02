import subprocess as sp
from .log import logger
from .log import handlers as H

class service :
    def __init__ (self, command, name, log_handlers=None,**wargs):
        if isinstance(H.base_handler) :
            log_handlers = [log_handlers]
        if log_handlers == None :
            log_handlers = []
        self.command = command
        self.name = name
        self.log = logger(name,*log_handlers,**wargs).log
        self.p = None
    def run(self):
        self.p = sp.Popen(self.command, shell=True, stdout=sp.PIPE)
        while True:
            try:
                self.p.wait(0.2)
                break
            except sp.TimeoutExpired:
                pass
            for line in self.p.stdout.readlines():
                self.log(line)
