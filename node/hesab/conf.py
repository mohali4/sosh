_cache = {}

def port ():
    if _cache.get('port', None) != None :
        return _cache['port']
    import psutil
    def check_ssh_port(port):
        for conn in psutil.net_connections():
            if conn.laddr.port == port: #type: ignore
                return True
        return False
    from django.conf import settings
    for port in settings.SSH_PORTS:
        if check_ssh_port(port):
            _cache['port'] = port
            return port
    return 'Error'

def myip ():
    if _cache.get('host',False):
        return _cache['host']
    else:
        import requests
        try:
            ip = requests.get('https://api.ipify.org').text
            _cache['host'] = ip
            return ip
        except:
            return 'Error'


def host():
    from django.conf import settings
    if settings.HOST : return settings.HOST
    return myip()



class List(list):
    def filter (self, key=lambda _ : True):
        ret = type(self)()
        for item in self :
            try:
                if key(item) :
                    ret.append(item)
            except:pass
        return ret
    def append(self, __object ) :
        super().append(__object)
        return self

