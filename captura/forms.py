from django.db import models
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory,modelformset_factory
from django.contrib.admin.widgets import AdminDateWidget
from models import objetivo,estrategia,meta,proyecto,accion,com_acc,com_pro,com_est,persona,problema
import datetime

ObjetivoForm = modelformset_factory(objetivo, fields=('nombre', 'autor', 'descripcion')) # falta peer
EstrategiaForm = modelformset_factory(estrategia, fields=('nombre', 'padre', 'descripcion', 'prob'))
MetaForm = modelformset_factory(meta, fields=('nombre', 'fecha', 'cuantificador', 'unidad', 'descripcion', 'padre'))
ProyectoForm = modelformset_factory(proyecto, fields=('nombre', 'padre', 'responsable', 'descripcion', 'necesita', 'prob'))
AccionForm = modelformset_factory(accion,fields=('nombre', 'padre', 'fecha', 'responsable', 'descripcion', 'necesita', 'avance', 'prob'))
PersonaForm = modelformset_factory(persona)
ProblemaForm = modelformset_factory(problema)
ComentEstForm = modelformset_factory(com_est)
ComentProForm = modelformset_factory(com_pro)
ComentAccForm = modelformset_factory(com_acc)

#objetivoForm = modelformset_factory(objetivo)
#estrategiaForm = modelformset_factory(estrategia)
#metaForm = modelformset_factory(meta)
#proyectoForm = modelformset_factory(proyecto)
#accionForm = modelformset_factory(accion)

Accioninline = inlineformset_factory(accion, com_acc, can_delete=True, extra=1)
Proyectoinline = inlineformset_factory(proyecto, com_pro, can_delete=False, extra=1)
Estrategiainline = inlineformset_factory(estrategia, com_est, can_delete=False, extra=1)

class accionForm(ModelForm):
    fecha = forms.DateField(widget=AdminDateWidget)
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
    fecha = forms.DateField(widget=AdminDateWidget)
    class Meta:
        model = meta
#        fields = ('fecha','cuantificador','activo')

class objetivoFrom(ModelForm):
    class Meta:
        model = objetivo
#        fields = ('descripcion','peer','activo')


def get_hex(algorithm, salt, raw_password):
        """
        Returns a string of the hexdigest of the given plaintext password and salt
        using the given algorithm ('md5', 'sha1' or 'crypt').
        """
        if algorithm == 'crypt':
            try:
                import crypt
            except ImportError:
                raise ValueError('"crypt" password algorithm not supported in this environment')
            return crypt.crypt(raw_password, salt)
        if algorithm == 'md5':
            import hashlib
            return hashlib.md5(salt + raw_password).hexdigest()
        elif algorithm == 'sha1':
            import hashlib
            return hashlib.sha1(salt + raw_password).hexdigest()
        raise ValueError("Got unknown password algorithm type in password.")


