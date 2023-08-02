from django.contrib import admin
from .models import vuser, period, transfer, node


def Remove (model,req,Q):
    for item in Q:
        item.delete()

class myModelAdmin(admin.ModelAdmin):
    actions=[Remove]
    


admin.site.register(vuser)
admin.site.register(period)
admin.site.register(transfer,myModelAdmin)
admin.site.register(node)
#admin.site.register(suser)