import psutil
from ..conf import port as __portgetter , List
from ..users import bridge
ssh_port = __portgetter()



def _ssh_iter ():

    for con in psutil.net_connections():
        if con.status == 'ESTABLISHED' and str(con.laddr.port) == str(ssh_port) :
            yield con

def ssh_list ():

    ssh_connections = List()
    for con in _ssh_iter():
        ssh_connections.append(con)
    return ssh_connections

def kill_connection(conn):
    for pr in psutil.process_iter() :
        if pr.pid == conn.pid : break
    print("killing" ,pr.username())
    pr.terminate()

def kill_ip (ip):
    for conn in _ssh_iter():
        if conn.raddr.ip == ip : break
    kill_connection(conn)


def by_users ():
    users = {}
    for prs in psutil.process_iter():
    #if True :
        try:
            connects = prs.connections(kind='inet')
            #connects = _ssh_iter()
            for con in connects:
                try:
                    if con.status == 'ESTABLISHED' and con.laddr.port == int(ssh_port):
                        if bridge.isuser(prs.username()):
                            username = bridge.toapp(prs.username())
                            users[username] = users.get(username, List()).append(con)
                except: 
                    pass
        except:
            pass
    return users

from django.conf import settings
import time

_cache = {
    'users':List([0,None])
}

def give_users ():
    cache = _cache['users']
    if time.time()-cache[0] > settings.CHECK_CONN_DELAY :
        cache[1] = by_users()
        cache[0] = time.time()
        return give_users()
    return _cache['users'][1]
