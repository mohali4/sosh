from .securety import secret
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
import json

def main (url):

    @url('list')
    @secret
    def list(request):
        from .models import access
        from json import dumps
        list = [acc.username for acc in access.objects.filter(secret=request.secret)]
        return HttpResponse(dumps(list), content_type='application/json')

    @url('create')
    @secret
    def create(request:HttpRequest):
        body = json.loads(request.body)
        from .models import access
        access.objects.create(secret=request.__dict__.get('secret'),**body)
        return HttpResponse('success')


    @url('delete')
    @secret
    def delete(request):
        from .models import access
        body = json.loads(request.body)
        access.objects.filter(secret=request.__dict__.get('secret'),**body).delete()
        return HttpResponse('success')

    @url('ip')
    @secret
    def ip(request):
        from .conf import myip
        return HttpResponse(str(myip()))


    @url('port')
    @secret
    def port(request):
        from .conf import port
        return HttpResponse (str(port()))

    @url('update')
    @secret
    def update(request):
        from .models import access
        print(request.__dict__.get('secret'))
        body = json.loads(request.body)
        q = access.objects.filter(secret=request.__dict__.get('secret'),username=body['username'])
        if not q.exists():
            obj = access.objects.create(secret=request.__dict__.get('secret'),**body)
        else:
            obj = q[0]
        if obj.password != body['password']:
            obj.password = body['password']
            obj.save()
        if obj.connections != body['connections'] :
            obj.connections = body['connections']
            obj.save()
        return HttpResponse('success')

    @url('onlines')
    @secret
    def onlines(request):
        from .models import access
        data = {acc.username: acc.onlines for acc in access.objects.filter(secret=request.__dict__.get('secret'))}
        return HttpResponse(json.dumps(data))

