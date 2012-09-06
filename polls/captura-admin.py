from captura.models import telefonos_persona,objetivo,meta,estrategia,proyecto,accion,alarma
from django.contrib.auth.models import User
from django.contrib import admin
from seguimiento.models import *

class EstrChoice(admin.TabularInline):
    model = com_est
    extra = 0

class ProbChoice(admin.TabularInline):
    model = com_pro
    extra = 1

class AcciChoice(admin.TabularInline):
    model = com_acc
    extra = 1

class EstrElije(admin.TabularInline):
    model = pro_est
    extra = 0

class ProbElije(admin.TabularInline):
    model = pro_pro
    extra = 1

class AcciElije(admin.TabularInline):
    model = pro_acc
    extra = 1

class Telefono(admin.ModelAdmin):
    list_display = ('persona', 'numero', 'tipo')
    list_filter = ['persona', 'tipo']

class Dependientes(admin.ModelAdmin):
    inlines = [EstrChoice]
    list_display = ('nombre', 'hijas')

class Roles(admin.ModelAdmin):
    list_display = ('objetivo','usuario','roles')

class Obj(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre','descripcion']}),
        ('Avanzado', {'fields': ['peer'], 'classes': ['collapse']})]
    def save_model(self, request, obj, form, change): 
	if not change:
	    obj.autor = request.user
        obj.save()
        instance = form.save(commit=False)
        if not hasattr(instance,'autor'):
            instance.autor = request.user.pk
        instance.save()
        form.save_m2m()
        return instance
    def save_formset(self, request, form, formset, change): 
        if not hasattr(instance,'autor'):
            instance.descripcion = request.user.pk
        instance.save()
        return formset.save()
    def queryset(self, request):
        custgroup = Group.objects.get(name="ejecutivo") 
        if custgroup in request.user.groups.all():
            return Entry.objects.all()
        return objetivo.objects.filter(autor=request.user)
    list_display = ('nombre', 'autor', 'descripcion', 'hijas','peer')

class Met(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre','descripcion','padre','fecha',('cuantificador','unidad')]}),
    list_display = ('nombre', 'avance', 'fecha', 'hijas')

class Pro(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre','descripcion','padre','responsable']}),
        ('Avanzado', {'fields': ['necesita','necesario'], 'classes': ['collapse']})]
    inlines = [ProbChoice]
    list_display = ('nombre', 'responsable', 'avance', 'hijas')

class Act(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre','descripcion','padre','responsable','fecha']}),
        ('Avanzado', {'fields': ['necesita','necesario'], 'classes': ['collapse']})]
    inlines = [AcciChoice]
    list_display = ('nombre', 'responsable', 'avance', 'fecha')

admin.site.register(objetivo, Obj)
admin.site.register(meta, Met)
admin.site.register(estrategia, Dependientes)
admin.site.register(proyecto, Pro)
admin.site.register(accion, Act)
admin.site.register(alarma)
admin.site.register(telefonos_persona, Telefono)
