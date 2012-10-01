from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.models import inlineformset_factory,modelformset_factory
from models import objetivo,estrategia,meta,proyecto,accion,pro_acc,pro_pro,pro_est
import datetime

ObjetivoForm = modelformset_factory(objetivo, fields=('nombre', 'autor', 'descripcion')) # falta peer
EstrategiaForm = modelformset_factory(estrategia, fields=('nombre', 'padre', 'descripcion'))#, widgets = {'nombre': Textarea(attrs={'cols': 100, 'rows': 1}), })
MetaForm = modelformset_factory(meta, fields=('nombre', 'fecha', 'cuantificador', 'unidad', 'descripcion', 'padre'))#, widgets = {'nombre': Textarea(attrs={'cols': 100, 'rows': 1}), })
ProyectoForm = modelformset_factory(proyecto, fields=('nombre', 'padre', 'responsable', 'descripcion', 'necesita', 'necesario'))
AccionForm = modelformset_factory(accion,fields=('nombre', 'padre', 'fecha', 'responsable', 'descripcion', 'necesita', 'necesario', 'avance'))

objetivoForm = modelformset_factory(objetivo)
#estrategiaForm = modelformset_factory(estrategia)
metaForm = modelformset_factory(meta)
proyectoForm = modelformset_factory(proyecto)
accionForm = modelformset_factory(accion)

Accioninline = inlineformset_factory(accion, pro_acc, can_delete=True, extra=1)
Proyectoinline = inlineformset_factory(proyecto, pro_pro, can_delete=False, extra=1)
Estrategiainline = inlineformset_factory(estrategia, pro_est, can_delete=False, extra=1)

class accionForm(ModelForm):
    class Meta:
        model = accion
#        fields = ('avance','fecha','responsable','activo')

class proyectoForm(ModelForm):
    class Meta:
        model = proyecto
#        fields = ('responsable','activo')

class estrategiaForm(ModelForm):
    class Meta:
        model = estrategia
        fields = ('nombre', 'padre', 'descripcion')
        
class metaForm(ModelForm):
    class Meta:
        model = meta
#        fields = ('fecha','cuantificador','activo')

class objetivoFrom(ModelForm):
    class Meta:
        model = objetivo
#        fields = ('descripcion','peer','activo')

