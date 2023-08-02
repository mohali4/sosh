from django.core.management.base import BaseCommand
from hesab.checks import run


    
class Command(BaseCommand):
    help = 'Run the checks loop'

    def handle(self, *args, **options):

        run()

