def _C (c:str,**wargs) -> str:
    import subprocess
    from shlex import split
    result = subprocess.run(split(c) , stdout=subprocess.PIPE, **wargs)
    return result.stdout.decode() #type: ignore

class bridge :

    def toapp (nameornames): #type: ignore
        if isinstance(nameornames,str):
            return nameornames[:-4]
        elif isinstance(nameornames,list) or isinstance(nameornames,tuple):
            return [bridge.toapp(name) for name in nameornames] #type: ignore


    def tolinux (nameornames): #type: ignore
        if isinstance(nameornames,str):
            return nameornames+"_vpn" #type: ignore
        elif isinstance(nameornames,list) or isinstance(nameornames,tuple):
            return [bridge.tolinux(name) for name in nameornames] #type: ignore

    def isuser (name:str): #type: ignore
        import re
        if re.match(r"^[a-zA-Z0-9]+_vpn$",name): #type: ignore
            return True
        return False



def status ():
    all_users = _C("cut -d: -f1 /etc/passwd").split()
    import re
    for user in all_users.copy():
        if not bridge.isuser(user): #type: ignore
            while user in all_users: all_users.remove(user)
    return bridge.toapp(all_users) #type: ignore
 
def create (name, passw):
    import os
    print(f'CREATING USER {name} WITH PASS {passw}')
    #passw_enc = _C(f'openssl passwd -1 {passw}')
    _C(f'useradd {bridge.tolinux(name)}') #type: ignore
    os.system(f'echo {bridge.tolinux(name)}:{passw} | chpasswd')
    #_C(f'usermod -L {bridge.tolinux(name)}')

def remove(name):
    print(f'DELETING USER {name}')
    _C(f'userdel -f {bridge.tolinux(name)}') #type: ignore

def exists (name):
    return name in status()

def update (name, passw):
    if exists(name):
        remove(name)
    create(name,passw)

def ensure_tobe (name,passw):
    if not exists(name) :
        create(name,passw)


def ensure_tonotbe (name):
    if exists(name) :
        remove(name)

import pwd

def uid (name):

    try:
        return pwd.getpwnam(bridge.tolinux(name)).pw_uid #type: ignore
    except:
        print('Error in get user uid')
        return 'Error'
