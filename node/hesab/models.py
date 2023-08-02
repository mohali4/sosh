from django.db import models
from datetime import datetime as dt , timedelta as td 
from .connections.ssh import give_users as connections


def _ (text:str): return text


def _now ():
    return  dt.now().date()

def amonth_after (): 
    
    return _now() + td(30)

def abit_later (): 

    return dt.now() + td(seconds=30)


def _secret ():
    from secrets import token_hex as gen
    return gen(1000)


class secret (models.Model):
    name = models.CharField(max_length=10)
    body = models.TextField(default=_secret)
    info = models.TextField(default="",blank=True)
    
    def hash(self) :
        from hashlib import sha1
        return sha1(self.body.encode()).hexdigest()
    def __str__ (self):
        return f"{self.name}: {self.hash()[:5]}"    

    @property
    def enabled (self) :
        return True
    


class access (models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    connections = models.IntegerField()
    secret = models.ForeignKey(secret, on_delete=models.CASCADE)

    @property
    def enabled (self):
        return True
    @property
    def uid (self):
        if self.enabled :
            return
        from .users import uid
        return uid(self.username)
        
    def linux_sync (self,rewrite=False):
        from .users import ensure_tonotbe ,ensure_tobe ,update
        if self.enabled :    #type: ignore
            if rewrite:
                update(self.username, self.password)
            else:
                ensure_tobe(self.username, self.password)
        else:
            ensure_tonotbe(self.username)

    def save (self, *args, **wargs):
        ret = super().save(*args, **wargs)
        self.linux_sync(rewrite=True)
        return ret

    @property
    def onlines (self) -> int:
        return connections().get(self.username,[]).__len__()

    def __str__ (self):
        return f"{self.secret.name}|| {self.username}:{self.connections}=>{self.onlines}"


