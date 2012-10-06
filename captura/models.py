from django.db import models
from django.contrib.auth.models import User#,AbstractUser
from django.forms import ModelForm
from django.forms.models import inlineformset_factory,modelformset_factory
import datetime

#
# Autenticacion
#
class telefonos_persona(models.Model):
    tipo = (
        ('C', 'Celular'),
        ('F', 'Fijo'),
    )
    numero = models.BigIntegerField(unique=True,verbose_name='Numero telefonico')
    tipo = models.CharField(max_length=1, choices=tipo)
    def __unicode__(self):
        return str(self.numero)

class persona(User):
    telefono = models.ForeignKey(telefonos_persona)
    def __unicode__(self):
        ng = self.get_full_name() + ' |' 
        for gr in self.groups.all() : ng += " "+str(gr)
        return ng

#
# Elementos de control y anotaciones
#
class unidad_meta(models.Model):
    numero = models.IntegerField(unique=True,verbose_name='Clave',editable=False)
    nombre = models.CharField(unique=True,max_length=45,verbose_name='Tipo de medicion')
    def __unicode__(self):
        return self.nombre

class problema(models.Model):
	severidad = ( 
		('A', 'Alta'),
		('B', 'Baja'),
        )
	autor = models.ForeignKey(persona,blank=True,null=True,editable=False)
	fecha = models.DateField('fecha',default=datetime.date.today(),editable=False)
	severidad = models.CharField(max_length=1, choices=severidad)
	descripcion = models.CharField(max_length=2000,verbose_name='Descripcion del problema')
	resuelto = models.BooleanField(default=False)
	def __unicode__(self):
             return self.descripcion

class comentario(models.Model):
    autor = models.ForeignKey(persona,blank=True,null=True)
    fecha = models.DateField('fecha',default=datetime.date.today())
    descripcion = models.CharField(max_length=2000,verbose_name='Comentario')
    def __unicode__(self):
        return self.descripcion

#
# Elementos de planeacion
#
class objetivo(models.Model):
    nombre = models.CharField(max_length=255,unique=True,verbose_name='Definicion')
    peer = models.ManyToManyField("self",blank=True,verbose_name='Objetivos Relacionados')
    descripcion = models.CharField(max_length=2000,blank=True,verbose_name='Descripcion')
    autor = models.ForeignKey(persona,verbose_name='Responsable')
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
        ns = ""
        for hij in cursor.fetchall():
                hs = meta.objects.get(pk=hij[0]).semaforo()
                if ( hs == "amarillo"):
                    ns = hs
                if ( hs == "rojo" ):
                    return hs
        if (ns == "" and cursor.fetchall()): return "verde"
        else: return "amarillo"
    def __unicode__(self):
        return self.nombre

class meta(models.Model):
    nombre = models.CharField(max_length=255,unique=True,verbose_name='Definicion')
    padre = models.ForeignKey(objetivo,verbose_name='Objetivo padre')
    fecha = models.DateField('fecha de cumplimiento')
    inicio = models.DateField('fecha de inicio',blank=True,default=datetime.date.today(),editable=False)
    autor = models.ForeignKey(persona,verbose_name='Responsable') #blank=True,null=True,editable=False)
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
        ns = ""
        for hij in cursor.fetchall():
                hs = estrategia.objects.get(pk=hij[0]).semaforo()
                if ( hs == "amarillo"):
                    ns = hs
                if ( hs == "rojo" ):
                    return hs
        if (ns == "" and cursor.fetchall()): return "verde"
        else: return "amarillo"
    def __unicode__(self):
        return self.nombre

class estrategia(models.Model):
    nombre = models.CharField(max_length=255,unique=True,verbose_name='Definicion')
    padre = models.ForeignKey(meta,verbose_name='Meta padre')
    descripcion = models.CharField(max_length=2000,blank=True,verbose_name='Descripcion')
    prob = models.ForeignKey(problema,blank=True,null=True,verbose_name='Problema')
    activo = models.BooleanField(default=True)
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
    def coments(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id 
            FROM captura_com_est
            WHERE %s IN ( sobre_id )
            """, [self.id])
        results = []
        for oll in cursor.fetchall():
            for o in oll:
                for no in accion.objects.filter(id__contains=o):
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
        ns = ""
        for hij in cursor.fetchall():
                hs = proyecto.objects.get(pk=hij[0]).semaforo()
                if ( hs == "amarillo"):
                    ns = hs
                if ( hs == "rojo" ):
                    return hs
        if (ns == "" and cursor.fetchall()): return "verde"
        else: return "amarillo"
    def __unicode__(self):
        return self.nombre

class proyecto(models.Model):
    nombre = models.CharField(max_length=255,unique=True,verbose_name='Definicion')
    padre = models.ForeignKey(estrategia,verbose_name='Estrategia padre')
    responsable = models.ForeignKey(persona,verbose_name='Lider')
    descripcion = models.CharField(max_length=2000,blank=True,verbose_name='Descripcion')
    necesita = models.ManyToManyField("self",blank=True,verbose_name='Necesita de')
    activo = models.BooleanField(default=True)
    prob = models.ForeignKey(problema,blank=True,null=True,verbose_name='Problema')
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
    def necesario(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id 
            FROM captura_proyecto
            WHERE %s IN ( necesita_id )
            """, [self.id])
        results = []
        for oll in cursor.fetchall():
            for o in oll:
                for no in accion.objects.filter(id__contains=o):
                    results.append(no)
        return results
    def coments(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id 
            FROM captura_com_pro
            WHERE %s IN ( sobre_id )
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
        ns = ""
        for hij in cursor.fetchall():
                hs = accion.objects.get(pk=hij[0]).semaforo()
                if ( hs == "amarillo"):
                    ns = hs
                if ( hs == "rojo" ):
                    return hs
        if (ns == "" and cursor.fetchall()): return "verde"
        else: return "amarillo"
    def __unicode__(self):
        return self.nombre

class accion(models.Model):
    nombre = models.CharField(max_length=255,unique=True,verbose_name='Definicion')
    padre = models.ForeignKey(proyecto,verbose_name='Proyecto padre')
    fecha = models.DateField('fecha de cumplimiento')
    inicio = models.DateField('fecha de inicio',blank=True,default=datetime.date.today(),editable=False)
    responsable = models.ForeignKey(persona,verbose_name='Responsable')
    descripcion = models.CharField(max_length=2000,blank=True,verbose_name='Descripcion')
    necesita = models.ManyToManyField("self",blank=True,verbose_name='Necesita de')
    avance = models.IntegerField(verbose_name='Porcentaje de avance',default='0')
    activo = models.BooleanField(default=True)
    prob = models.ForeignKey(problema,blank=True,null=True,verbose_name='Problema')
    def coments(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id 
            FROM captura_com_acc
            WHERE %s IN ( sobre_id )
            """, [self.id])
        results = []
        for oll in cursor.fetchall():
            for o in oll:
                for no in accion.objects.filter(id__contains=o):
                    results.append(no)
        return results
    def necesario(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id 
            FROM captura_accion
            WHERE %s IN ( necesita_id )
            """, [self.id])
        results = []
        for oll in cursor.fetchall():
            for o in oll:
                for no in accion.objects.filter(id__contains=o):
                    results.append(no)
        return results
    def semaforo(self):
        delta = datetime.date.today()-self.inicio
        total = self.fecha-self.inicio 
        if ((self.avance < 50) and (float(delta.total_seconds()) < float(total.total_seconds())*0.8)) or (self.prob == "A"):
            return "rojo"
        if (float(total.total_seconds())*self.avance/100 > float(delta.total_seconds())) or (not self.prob == "B"):
            return "verde"
        return "amarillo"
    def __unicode__(self):
        return self.nombre

#
# Comentarios por elemento
#
class com_est(comentario):
	sobre = models.ForeignKey(estrategia)
	def __unicode__(self):
             return self.descripcion

class com_pro(comentario):
	sobre = models.ForeignKey(proyecto)
	def __unicode__(self):
             return self.descripcion

class com_acc(comentario):
	sobre = models.ForeignKey(accion)
	def __unicode__(self):
            return self.descripcion

