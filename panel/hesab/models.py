from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import UserManager
from jdatetime import datetime as jdt , timedelta as jtd , date as jd
from django.utils.functional import lazy


def _ (text:str): return text


class myUserManager(UserManager):
    def create_user(self,username,phonenumber=None,**etc):
        return super().create_user(username,phonenumber=phonenumber,**etc)


class transfer_queryset(models.QuerySet):
    def enableds (self):
        ret = self
        for item in self :
            if not item.enable :
                ret = ret.exclude(id=item.id)
        return ret


    def delete(self) :
        #print('deleting')
        for item in self:
            item.ensure_tonotbe()
        return super().delete()


class transfer_manager(models.Manager):    

    def get_queryset(self):
        return transfer_queryset(self.model,using=self._db)

    def enableds(self):
        return self.get_queryset().enableds()

def _now ():
    return  jdt.now().date()
def amonth_after (): 
    
    return _now() + jtd(30)

def _password ():
    from secrets import token_hex as gen
    return gen(5)



class period (models.Model):
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
    name = models.CharField(max_length=10)
    days = models.IntegerField()
    value = models.IntegerField()
    users = models.IntegerField()
    info = models.TextField(blank=True,default=None)

    def __str__ (self) :
        return f"{self.name}: ({self.value}tom->{self.days}days)   {self.users}U"


class transfer (models.Model):

    class Meta :
        verbose_name = "خرید"
        verbose_name_plural = "خریدها"

    user = models.ForeignKey("vuser",verbose_name='کاربر' , on_delete=models.CASCADE)
    period = models.ForeignKey("period",verbose_name='محصول' , on_delete=models.PROTECT)
    node = models.ForeignKey('node',verbose_name='سرور' , on_delete=models.PROTECT)
    password = models.CharField(max_length=15,default=_password)
    payed = models.BooleanField('پرداخت',default=False)
    fake_payed = models.BooleanField('در هر صورت فعال شود',default=True)
    start = jmodels.jDateField('شروع',default=_now) #type:ignore
    @property
    def end  (self): return jdt.date (self.start + jtd(self.period.days)) 
    info = models.TextField('توضیحات',default=None,blank=True)
    config = models.TextField('کانفیگ',blank=True,default="")

    objects = transfer_manager()

    @property
    def username (self): 
        return self.user.name

    @property
    def connections (self):
        return self.period.users

    @property
    def enable (self) -> bool:
        if not (self.payed or self.fake_payed ):
            return False
        if self.end < _now() :
            return False
        return True

    def ensure_tobe(self):
        self.node.ensure_tobe(self)

    def ensure_tonotbe(self):
        self.node.ensure_tonotbe(self)

    def gen_config(self):
        from .users import bridge
        host = self.node.ssh_host
        port = self.node.ssh_port
        username = bridge.tolinux (self.user.name) #type: ignore
        password = self.password 
        return f'''
NapsternetV:
bitvisessh:
    host={host}
    port={port}
    username={username}
    password={password}

HttpCustom:
    {host}:{port}@{username}:{password}
'''

    def setconfig(self):
        self.config = self.gen_config()
        self.save(notconfgen=True)

    def sync (self):
        if self.enable :
            self.node.sync(self)
        else:
            self.node.delete_acc(self)

    def save(self,**wargs):
        mywargs = {}
        if 'notconfgen' in wargs :
            mywargs['notconfgen'] = wargs['notconfgen']
            del wargs['notconfgen']

        ret = super().save(**wargs)

        self.sync()

        if not mywargs.get('notconfgen',False):
            self.setconfig()
        
        return ret

    def delete(self, **w):
        #print('deleting')
        self.ensure_tonotbe()
        ret = super().delete(**w)
        return ret

    @property
    def onlines(self):
        return self.node.onlines_data.get(self.username,0)

    def __str__ (self) :
        return f"{self.user.__str__()} {self.period.users}->{self.node.name}:{self.onlines} || {self.end.year}/{self.end.month}/{self.end.day}     {':)' if self.payed else ':('}"



class vuser (models.Model):

    class Meta :
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    name = models.CharField(max_length=15)
    phonenumber = models.CharField(max_length=13,blank=True)
    info = models.TextField(blank=True)
    
    @property
    def enable (self) -> bool :
        return transfer.objects.filter(user=self,payed=True).enableds().exists()

    def __str__ (self):
        return self.name




class node (models.Model):
    class Meta:
        verbose_name = "سرور"
        verbose_name_plural ="سرورها"
    
    name = models.CharField(max_length=10)
    host = models.CharField(max_length=100)
    port = models.IntegerField(default=2222)
    secret = models.TextField()
    info = models.TextField(default='',blank=True)
    ssh_hostname = models.CharField(default=None,blank=True,max_length=30)

    @property
    def transfers (self) :
        return transfer.objects.filter(node=self)

    @property
    def api(self):
        class _api :
            def __init__ (self,_node):
                self._node = _node
            def __getattribute__(self, __name: str):
                from . import api
                def func (*args,**wargs):
                    f = api.__dict__[__name]
                    return f(self._node,*args,**wargs)
                if __name in api.__all__ :
                    return func
                return super().__getattribute__(__name)
        return _api(self)

    @property
    def ssh_port(self):
        return self.api.port()    
    
    @property
    def ssh_host(self):
        if self.ssh_hostname:
            return self.ssh_hostname
        return self.api.ip()
    
    def hash(self):
        from hashlib import sha1
        return sha1(self.secret.encode()).hexdigest()

    @property
    def address (self):
        return f"{self.host}:{self.port}"

    def sync (self, access):
        r = self.api.update(
            username=access.username,
            password=access.password,
            connections=access.connections
            )
        if not r :
            print('An Error in node.sync')

    def delete_acc (self,acc):
        r = self.api.delete(
            username = acc.username
        )
        if not r:
            print('An Error in node.delete_acc')
    
    def list(self):
        return self.api.list()

    def ensure_tobe(self,acc) :
        return self.sync(acc)
    
    def ensure_tonotbe(self,acc):
        return self.delete_acc(acc)

    @property
    def onlines_data (self):
        return self.get_onlines_data()
    
    @property
    def onlines_len (self):
        data = self.onlines_data
        _len = 0
        for _, p in data.items():
            _len += p
        return  _len

    def get_onlines_data(self):
        from .conf import cache
        try:
            self.__dict__['__onlines_cache'] = self.__dict__.get('__onlines_cache',cache(self.api.onlines,60))
            resp = self.__dict__['__onlines_cache']()
            if resp == None :
                raise
            return resp
        except:
            return {}


    def __str__ (self):
        account_len = 0
        for acc in self.transfers.enableds() :
            account_len += acc.connections 
        return f"{self.name}({self.address}): {self.hash()[:5]}  || {account_len}=>{self.onlines_len}"
    