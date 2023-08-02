from .list import loop
from jdatetime import datetime
def run ():
    for name ,operation in loop :
        print (f"{name}({datetime.now().isoformat()}): ",end='')
        try : 
            operation()
            print (f'{name} operation SUCCEEDED')
        except:
            print (f'{name} operation FAILED')

