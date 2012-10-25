from captura.models import telefonos_persona,persona,objetivo,meta,estrategia,proyecto,accion,unidad_meta,persona,comentario,problema,com_est,com_pro,com_acc
from django.contrib import admin
from django.contrib.auth.models import Group

class EstrChoice(admin.TabularInline):
    model = com_est
    extra = 0

class ProyChoice(admin.TabularInline):
    model = com_pro
    extra = 0

class AcciChoice(admin.TabularInline):
    model = com_acc
    extra = 0

class Telefono(admin.ModelAdmin):
    list_display = ('persona', 'telefono')

class Est(admin.ModelAdmin):
    inlines = [EstrChoice]
    list_display = ('nombre', 'hijas')

class Obj(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre','descripcion']}),
        ('Avanzado', {'fields': ['peer','activo','autor'], 'classes': ['collapse']})]
    def save_model(self, request, obj, form, change): 
	if not change:
	    obj.autor = request.user
        obj.save()
    def save_formset(self, request, form, formset, change): 
        if not hasattr(instance,'autor'):
            instance.descripcion = request.user.pk
        instance.save()
        return formset.save()
    def queryset(self, request):
        custgroup = Group.objects.get(name="ejecutivo") 
        if custgroup in request.user.groups.all():
            return objetivo.objects.all()
        return objetivo.objects.filter(autor=request.user)
    list_display = ('nombre', 'autor', 'activo', 'hijas')

class Met(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre','descripcion','padre','fecha',('cuantificador','unidad')]}),
        ('Avanzado', {'fields': ['activo','autor'], 'classes': ['collapse']})]
    def save_model(self, request, obj, form, change): 
	if not change:
	    obj.autor = request.user
        obj.save()
    def save_formset(self, request, form, formset, change): 
        if not hasattr(instance,'autor'):
            instance.descripcion = request.user.pk
        instance.save()
        return formset.save()
    def queryset(self, request):
        custgroup = Group.objects.get(name="ejecutivo") 
        if custgroup in request.user.groups.all():
            return meta.objects.all()
        return meta.objects.filter(autor=request.user)
    list_display = ('nombre', 'avance', 'fecha', 'activo', 'hijas')

class Pro(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre','descripcion','padre','responsable']}),
        ('Avanzado', {'fields': ['prob','necesita','activo'], 'classes': ['collapse']})]
    inlines = [ProyChoice]
    def queryset(self, request):
        custgroup = Group.objects.get(name="ejecutivo") 
        if custgroup in request.user.groups.all():
            return proyecto.objects.all()
        return proyecto.objects.filter(responsable=request.user)
    list_display = ('nombre', 'responsable', 'activo', 'avance', 'hijas')

class Act(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre','descripcion','padre','responsable','fecha','avance']}),
        ('Avanzado', {'fields': ['prob','necesita','activo'], 'classes': ['collapse']})]
    inlines = [AcciChoice]
    def queryset(self, request):
        custgroup = Group.objects.get(name="ejecutivo") 
        if custgroup in request.user.groups.all():
            return accion.objects.all()
        return accion.objects.filter(responsable=request.user)
    list_display = ('nombre', 'responsable', 'activo', 'avance', 'fecha')

admin.site.register(objetivo, Obj)
admin.site.register(meta, Met)
admin.site.register(estrategia, Est)
admin.site.register(proyecto, Pro)
#admin.site.register(accion)
admin.site.register(accion, Act)
#admin.site.register(unidad_meta)
admin.site.register(persona, Telefono)
admin.site.register(problema)
