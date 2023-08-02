
class logger :
    def __init__ (self, name, *handlers, **wargs):
        self.name = name
        self.stack = list()
        self.handlers = handlers

    def log (self,text:str):
        for line in text.split('\n'):
            line = line.strip()
            if not line == '':
                self.stack.append(line)
        self.exclude()

    def exclude (self):
        for line in self.stack:
            for handler in self.handlers:
                handler(line)
        self.stack = []
