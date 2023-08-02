import os

class base_handler:
    def __call__(self,line):
        pass

class file (base_handler) :
    def __init__ (self,Path):
        self.path = Path
    def __call__ (self,line):
        try:
            if not os.path.exists(self.path) :
                os.system(f"touch {self.path}")
            with open(self.path, 'a+') as f:
                f.write(line)
                f.close()
        except:
            print(f"Error in write LOG in file {self.path}")
    
