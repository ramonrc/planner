from django.db import models
from django.contrib.auth.models import User
from captura.models import *
import datetime

# Create your models here.
class comentario(models.Model):
    autor = models.ForeignKey(User,blank=True,null=True)
    fecha = models.DateField('fecha',default=datetime.date.today())
    descripcion = models.CharField(max_length=2000,verbose_name='Comentario')
    def __unicode__(self):
        return self.descripcion

class com_est(models.Model):
	sobre = models.ForeignKey(estrategia)
	coment = models.ForeignKey(comentario,verbose_name='Comentarios')
	def __unicode__(self):
             return self.coment.descripcion

class com_pro(models.Model):
	sobre = models.ForeignKey(proyecto)
	coment = models.ForeignKey(comentario,verbose_name='Comentarios')
	def __unicode__(self):
             return self.coment.descripcion

class com_acc(models.Model):
	sobre = models.ForeignKey(accion)
	coment = models.ForeignKey(comentario,verbose_name='Comentarios')
	def __unicode__(self):
             return self.coment.descripcion

