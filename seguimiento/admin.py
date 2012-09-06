from django.contrib import admin
#from captura.models import *
from seguimiento.models import *

class EstrChoice(admin.TabularInline):
    model = com_est
    extra = 0

class ProbChoice(admin.TabularInline):
    model = com_pro
    extra = 0

class AcciChoice(admin.TabularInline):
    model = com_acc
    extra = 0

class Com(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['coment']})]
    def save_model(self, request, obj, form, change):
        if not change:
            obj.comentario.autor = request.user
        obj.save()


#admin.site.register(problema)
admin.site.register(comentario)
#admin.site.register(com_est, Com)
#admin.site.register(com_pro, Com)
#admin.site.register(com_acc, Com)
