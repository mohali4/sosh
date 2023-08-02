from . import checks
from django.conf import settings
loop = []
def func ():...
function = type(func)
for name,c in checks.__dict__.items():
    if isinstance(c,function):
        if c.__dict__.get('loop',False):
            if name in settings.CHECK_LIST:
                loop.append((name,c))