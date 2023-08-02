from django.core.management.base import BaseCommand
import time
from django.conf import settings

from ...checks import run


    
class Command(BaseCommand):
    help = 'Run the checks loop'

    def handle(self, *args, **options):
        while True:

            run()

            try : time.sleep(settings.CHECK_DELAY)
            except:
                print("EXITTING...")
                quit()
