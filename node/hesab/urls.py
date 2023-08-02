from django.urls import path

urlpatterns = []

def url (pattern):
    def decorate (func):
        urlpatterns.append(path(pattern,func))
        return func
    return decorate

from .api import main
main(url)