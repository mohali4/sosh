from ..models import access
from ..users import status, remove
from django.conf import settings
check_list = []
def append (time=settings.CHECK_DELAY):
    def add (f):
        check_list.append(f)
        f.__dict__['last_run'] = 0
        f.__dict__['delay'] = time
    return add

@append()
def check_access ():
    for acc in access.objects.all(): 
        acc.linux_sync()

@append(settings.CHECK_DELAY)
def check_linux ():
    def _remove(user):
        remove(user)
    for user_name in status(): #type: ignore
        Fuser = access.objects.filter(username=user_name)
        if not Fuser.exists():            
            _remove(user_name)
        else: 
            user = Fuser[0]
            if not user.enabled :
                _remove(user_name)


from ..models import access
from ..connections.ssh import give_users, kill_ip
from ..conf import List

    
@append(2)
def check_connections ():
    connections = give_users()
    #print(connections)
    for acc in access.objects.all():
        if acc.enabled :
            uconnections = connections.get(acc.username,List())
            print(acc.username,len(uconnections))
            if uconnections.__len__() > acc.connections :
                for conn in uconnections : kill_ip(conn.raddr.ip)

