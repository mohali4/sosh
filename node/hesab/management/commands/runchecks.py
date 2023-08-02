from django.core.management.base import BaseCommand
import time
from jdatetime import datetime
from ...checks import check_list

class Command(BaseCommand):
    help = 'Run the checks'

    def handle(self, *args, **options):
        
        for chck in check_list :
            if chck.__dict__['delay'] < time.time() - chck.__dict__['last_run']:
                print (f"{chck.__name__}({datetime.now().isoformat()}): ",end='\n')
                try : 
                    chck()
                    print (f'{chck.__name__} operation SUCCEEDED')
                except:
                    #chck()
                    print (f'{chck.__name__} operation FAILED')
