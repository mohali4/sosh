from django.contrib import admin
from .models import access, secret


admin.site.register(secret)
admin.site.register(access)
#admin.site.register(suser)