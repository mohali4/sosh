from django.core.management.base import BaseCommand
import time
from jdatetime import datetime
from ...checks import check_access, check_linux, check_list
from django.conf import settings

class Command(BaseCommand):
    help = 'Run the checks loop'

    def handle(self, *args, **options):
        while True:
            for chck in check_list :
                if chck.__dict__['delay'] < time.time() - chck.__dict__['last_run']:
                    print (f"{chck.__name__}({datetime.now().isoformat()}): ",end='\n')
                    chck.__dict__['last_run'] = time.time()
                    try : 
                        chck()
                        print (f'{chck.__name__} operation SUCCEEDED')
                    except:
                        print (f'{chck.__name__} operation FAILED')

    
            try : time.sleep(1)
            except:
                print("EXITTING...")
                quit()
