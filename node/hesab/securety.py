from django.http import HttpRequest, HttpResponseNotAllowed

def secret_vallidation(secret_body):
    from .models import secret
    sec = secret.objects.get(body=secret_body)
    return sec
    

def secret (func):
    from django.views.decorators.csrf import csrf_exempt as disable_csrf
    @disable_csrf
    def _func (request:HttpRequest, *args, **kwargs):
        try:
            secret = request.headers['mohali_secret']
            secret = secret_vallidation(secret)
            vallid = secret.enabled #tpye: ignore
        except:
            vallid = False
        finally:
            if not vallid :
                return HttpResponseNotAllowed("secret validation failed")
        
        request.__dict__['secret'] = secret #type: ignore

        return func(request, *args, **kwargs)
    return _func


