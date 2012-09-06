from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class roles_persona(models.Model):
    numero = models.IntegerField(unique=True,verbose_name='Clave')
    nombre = models.CharField(max_length=45,verbose_name='Rol')
    def __unicode__(self):
        return self.nombre

class telefonos_persona(models.Model):
    tipo = (
        ('C', 'Celular'),
        ('F', 'Fijo'),
    )
    persona = models.ForeignKey(User,unique=True)
    numero = models.BigIntegerField(unique=True,verbose_name='Numero telefonico')
    tipo = models.CharField(max_length=1, choices=tipo)

class status_objetivo(models.Model):
    numero = models.IntegerField(unique=True,verbose_name='Clave')
    nombre = models.CharField(max_length=45,verbose_name='Status')
    def __unicode__(self):
        return self.nombre

class objetivo(models.Model):
    nombre = models.CharField(max_length=255,unique=True,verbose_name='Definicion')
    status = models.ForeignKey(status_objetivo)
    peer = models.ManyToManyField("self",blank=True,verbose_name='Objetivos Relacionados')
    descripcion = models.CharField(max_length=2000,blank=True,verbose_name='Descripcion')
    autor = models.ForeignKey(User,blank=True,default='0')
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
                    results.append(no.id)
        return results
#    def clean(self):
#        from django.core.exceptions import ValidationError
#	self.autor = request.user
    def __unicode__(self):
        return self.nombre

class roles_objetivo(models.Model):
    usuario = models.ForeignKey(User,unique=True)
    objetivo = models.ForeignKey(objetivo) 
    rol = models.ManyToManyField(roles_persona,blank=True,related_name='rols')
    def roles(self):
        return self.rol.all()

class unidad_meta(models.Model):
    numero = models.IntegerField(unique=True,verbose_name='Clave')
    nombre = models.CharField(unique=True,max_length=45,verbose_name='Tipo de medicion')
    def __unicode__(self):
        return self.nombre

class meta(models.Model):
    nombre = models.CharField(max_length=255,unique=True,verbose_name='Definicion')
    padre = models.ForeignKey(objetivo,verbose_name='Objetivo padre')
    fecha = models.DateField('fecha de cumplimiento')
    inicio = models.DateField('fecha de inicio',blank=True,default=datetime.date.today())
    cuantificador = models.IntegerField()
    unidad = models.ForeignKey(unidad_meta,verbose_name='Tipo de medicion')
    descripcion = models.CharField(max_length=2000,blank=True,verbose_name='Descripcion')
    avance = models.IntegerField(verbose_name='Porcentaje de avance',default='0')
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
                    results.append(no.id)
        return results
    def __unicode__(self):
        return self.nombre

class estrategia(models.Model):
    nombre = models.CharField(max_length=255,unique=True,verbose_name='Definicion')
    padre = models.ForeignKey(meta,verbose_name='Meta padre')
    descripcion = models.CharField(max_length=2000,blank=True,verbose_name='Descripcion')
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
                    results.append(no.id)
        return results
    def __unicode__(self):
        return self.nombre

class proyecto(models.Model):
    nombre = models.CharField(max_length=255,unique=True,verbose_name='Definicion')
    padre = models.ForeignKey(meta,verbose_name='Estrategia padre')
    responsable = models.ForeignKey(User,verbose_name='Lider')
    descripcion = models.CharField(max_length=2000,blank=True,verbose_name='Descripcion')
    necesita = models.ManyToManyField("self",blank=True,verbose_name='Necesita de')
    necesario = models.ManyToManyField("self",blank=True,verbose_name='Es necesrio para')
    avance = models.IntegerField(verbose_name='Porcentaje de avance',default='0')
    activo = models.BooleanField(default=True)
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
                    results.append(no.id)
        return results
    def __unicode__(self):
        return self.nombre

class accion(models.Model):
    nombre = models.CharField(max_length=255,unique=True,verbose_name='Definicion')
    padre = models.ForeignKey(proyecto,verbose_name='Proyecto padre')
    fecha = models.DateField('fecha de cumplimiento')
    inicio = models.DateField('fecha de inicio',blank=True,default=datetime.date.today())
    responsable = models.ForeignKey(User,verbose_name='Responsable')
    descripcion = models.CharField(max_length=2000,blank=True,verbose_name='Descripcion')
    necesita = models.ManyToManyField("self",blank=True,verbose_name='Necesita de')
    necesario = models.ManyToManyField("self",blank=True,verbose_name='Es necesrio para')
    avance = models.IntegerField(verbose_name='Porcentaje de avance',default='0')
    activo = models.BooleanField(default=True)
    def __unicode__(self):
        return self.nombre

class alarma(models.Model):
    valor = models.IntegerField()
    meta = models.ForeignKey(meta,unique=True)
    def __unicode__(self):
        return self.meta.nombre

