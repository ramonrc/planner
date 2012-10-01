from django.db import models
from django.contrib.auth.models import User #AbstractUser
from django.forms import ModelForm
from django.forms.models import inlineformset_factory,modelformset_factory
import datetime

# Create your models here.
class telefonos_persona(models.Model):
    tipo = (
        ('C', 'Celular'),
        ('F', 'Fijo'),
    )
    persona = models.ForeignKey(User,unique=True)
    numero = models.BigIntegerField(unique=True,verbose_name='Numero telefonico')
    tipo = models.CharField(max_length=1, choices=tipo)

class persona(User):
    telefono = models.ForeignKey(telefonos_persona,related_name='persona_telefono')

class objetivo(models.Model):
    nombre = models.CharField(max_length=255,unique=True,verbose_name='Definicion')
    peer = models.ManyToManyField("self",blank=True,verbose_name='Objetivos Relacionados')
    descripcion = models.CharField(max_length=2000,blank=True,verbose_name='Descripcion')
    autor = models.ForeignKey(User,verbose_name='Responsable')
    activo = models.BooleanField(default=True)
    def hijas(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id 
            FROM captura_meta 
            WHERE %s IN ( padre_id )
            """, [self.id])
        results = []
        for oll in cursor.fetchall():
            for o in oll:
                for no in meta.objects.filter(id__contains=o):
                    results.append(no)
        return results
    def semaforo(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id
            FROM captura_meta
            WHERE %s IN ( padre_id )
            """, [self.id])
        for hija in cursor.fetchall():
            for hij in hija:
                for hi in meta.objects.filter(id__contains=hij):
                    if ( hi.semaforo == "alto" ):
                        return hi.semaforo
                    if ( hi.semaforo == "amarillo" ):
                        return hi.semaforo
        return "siga"
    def __unicode__(self):
        return self.nombre

class unidad_meta(models.Model):
    numero = models.IntegerField(unique=True,verbose_name='Clave',editable=False)
    nombre = models.CharField(unique=True,max_length=45,verbose_name='Tipo de medicion')
    def __unicode__(self):
        return self.nombre

class meta(models.Model):
    nombre = models.CharField(max_length=255,unique=True,verbose_name='Definicion')
    padre = models.ForeignKey(objetivo,verbose_name='Objetivo padre')
    fecha = models.DateField('fecha de cumplimiento')
    inicio = models.DateField('fecha de inicio',blank=True,default=datetime.date.today(),editable=False)
    autor = models.ForeignKey(User,verbose_name='Responsable') #blank=True,null=True,editable=False)
    cuantificador = models.IntegerField()
    unidad = models.ForeignKey(unidad_meta,verbose_name='Tipo de medicion')
    descripcion = models.CharField(max_length=2000,blank=True,verbose_name='Descripcion')
    activo = models.BooleanField(default=True)
    def hijas(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id 
            FROM captura_estrategia
            WHERE %s IN ( padre_id )
            """, [self.id])
        results = []
        for oll in cursor.fetchall():
            for o in oll:
                for no in estrategia.objects.filter(id__contains=o):
                    results.append(no)
        return results
    def avance (self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id 
            FROM captura_estrategia
            WHERE %s IN ( padre_id )
            """, [self.id])
        av = 0
        count = 0
        for oll in cursor.fetchall():
            for o in oll:
                for no in estrategia.objects.filter(id__contains=o):
                    for ol in no.hijas():
                        for o in ol.hijas():
                            count = count + 1
                            av =+ o.avance
        if ( count == 0 ):
            return "no hay accion"
        return av/count
    def semaforo(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id 
            FROM captura_estrategia
            WHERE %s IN ( padre_id )
            """, [self.id])
        for hija in cursor.fetchall():
            for hij in hija:
                for hi in estrategia.objects.filter(id__contains=hij):
                    if ( hi.semaforo == "alto" ):
                        return "alto"
                    if ( hi.semaforo == "amarillo" ):
                        return "amarillo"
        return "siga"
    def __unicode__(self):
        return self.nombre

class problema(models.Model):
	severidad = ( 
		('A', 'Alta'),
		('B', 'Baja'),
        )
	autor = models.ForeignKey(User,blank=True,null=True,editable=False)
	fecha = models.DateField('fecha',default=datetime.date.today(),editable=False)
	severidad = models.CharField(max_length=1, choices=severidad)
	descripcion = models.CharField(max_length=2000,verbose_name='Descripcion del problema')
	resuelto = models.BooleanField(default=False)
	def __unicode__(self):
             return self.descripcion

class estrategia(models.Model):
    nombre = models.CharField(max_length=255,unique=True,verbose_name='Definicion')
    padre = models.ForeignKey(meta,verbose_name='Meta padre')
    descripcion = models.CharField(max_length=2000,blank=True,verbose_name='Descripcion')
#    prob = models.ForeignKey(problema,verbose_name='Problema')
#    activo = models.BooleanField(default=True)
    def hijas(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id 
            FROM captura_proyecto
            WHERE %s IN ( padre_id )
            """, [self.id])
        results = []
        for oll in cursor.fetchall():
            for o in oll:
                for no in proyecto.objects.filter(id__contains=o):
                    results.append(no)
        return results
    def semaforo(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id 
            FROM captura_proyecto
            WHERE %s IN ( padre_id )
            """, [self.id])
        for hija in cursor.fetchall():
            for hij in hija:
                for hi in proyecto.objects.filter(id__contains=hij):
                    if ( hi.semaforo == "alto" ):
                        return "alto"
                    if ( hi.semaforo == "amarillo" ):
                        return "amarillo"
        return "siga"
    def __unicode__(self):
        return self.nombre

class proyecto(models.Model):
    nombre = models.CharField(max_length=255,unique=True,verbose_name='Definicion')
    padre = models.ForeignKey(estrategia,verbose_name='Estrategia padre')
    responsable = models.ForeignKey(User,verbose_name='Lider')
    descripcion = models.CharField(max_length=2000,blank=True,verbose_name='Descripcion')
    necesita = models.ManyToManyField("self",blank=True,verbose_name='Necesita de')
    necesario = models.ManyToManyField("self",blank=True,verbose_name='Es necesrio para')
    activo = models.BooleanField(default=True)
#    prob = models.ForeignKey(problema,verbose_name='Problema')
    def hijas(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id 
            FROM captura_accion
            WHERE %s IN ( padre_id )
            """, [self.id])
        results = []
        for oll in cursor.fetchall():
            for o in oll:
                for no in accion.objects.filter(id__contains=o):
                    results.append(no)
        return results
    def avance (self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id 
            FROM captura_accion
            WHERE %s IN ( padre_id )
            """, [self.id])
        av = 0
        count = 0
        for oll in cursor.fetchall():
            for o in oll:
                for no in accion.objects.filter(id__contains=o):
                    count = count + 1
                    av =+ no.avance
        if ( count == 0 ):
            return "no hay accion"
        return av/count
    def semaforo(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id 
            FROM captura_accion
            WHERE %s IN ( padre_id )
            """, [self.id])
        for hija in cursor.fetchall():
            for hij in hija:
                for hi in accion.objects.filter(id__contains=hij):
                    if ( hi.semaforo == "alto" ):
                        return "alto"
                    if ( hi.semaforo == "amarillo" ):
                        return "amarillo"
        return "siga"
    def __unicode__(self):
        return self.nombre

class accion(models.Model):
    nombre = models.CharField(max_length=255,unique=True,verbose_name='Definicion')
    padre = models.ForeignKey(proyecto,verbose_name='Proyecto padre')
    fecha = models.DateField('fecha de cumplimiento')
    inicio = models.DateField('fecha de inicio',blank=True,default=datetime.date.today(),editable=False)
    responsable = models.ForeignKey(User,verbose_name='Responsable')
    descripcion = models.CharField(max_length=2000,blank=True,verbose_name='Descripcion')
    necesita = models.ManyToManyField("self",blank=True,verbose_name='Necesita de')
    necesario = models.ManyToManyField("self",blank=True,verbose_name='Es necesrio para')
    avance = models.IntegerField(verbose_name='Porcentaje de avance',default='0')
    activo = models.BooleanField(default=True)
#    prob = models.ForeignKey(problema,verbose_name='Problema')
    def semaforo(self):
        if self.avance < 50 and (today-self.inicio)/(self.fecha-self.inicio) < 0.8:
            return "rojo"
        if self.avance/100 < (today-self.inicio)/(self.fecha-self.inicio):
            return "amarillo"
        return "verde"
    def __unicode__(self):
        return self.nombre

class pro_est(models.Model):
	sobre = models.ForeignKey(estrategia)
	problema = models.ForeignKey(problema,verbose_name='Problemas')
	def __unicode__(self):
             return self.problema.descripcion

class pro_pro(models.Model):
	sobre = models.ForeignKey(proyecto)
	problema = models.ForeignKey(problema,verbose_name='Problemas')
	def __unicode__(self):
             return self.problema.descripcion

class pro_acc(models.Model):
	sobre = models.ForeignKey(accion)
	problema = models.ForeignKey(problema,verbose_name='Problemas')
	def __unicode__(self):
             return self.problema.descripcion
