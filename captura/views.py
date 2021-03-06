from django.http import HttpResponse,HttpResponseRedirect
from django.utils.html import escape
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from django.contrib.auth import logout
from django.template import RequestContext
from django.core.mail import send_mail
from django.utils.encoding import smart_unicode
from models import *
from forms import *

burl = "/goremo/"

def logout_page(request):
   logout(request)
   return HttpResponseRedirect(burl)

@login_required(login_url = burl + "accounts/login/")
#@login_required()
def inicio(request): # dependiendo del grupo aque esta asignado el usuario
    custgroup = Group.objects.get(name="ejecutivo") 
    if custgroup in request.user.groups.all():
        custgroup = Group.objects.get(name="manager") 
        ps = objetivo.objects.filter(activo=True).order_by("id")
        if custgroup in request.user.groups.all(): # si es manageer y ejecutivo entra como manager
           return render_to_response('plan/manager.html', {'ol' : ps, 'bu' : burl }, context_instance=RequestContext(request))
        return render_to_response('plan/ejecutivo.html', {'ol' : ps, 'bu' : burl }, context_instance=RequestContext(request))
    custgroup = Group.objects.get(name="manager") 
    if custgroup in request.user.groups.all():
        ps = objetivo.objects.filter(autor=request.user).filter(activo=True).order_by("id")
        return render_to_response('plan/manager.html', {'ol' : ps, 'bu' : burl }, context_instance=RequestContext(request))
    custgroup = Group.objects.get(name="lider") 
    if custgroup in request.user.groups.all():
        custgroup = Group.objects.get(name="responsable")
        if custgroup in request.user.groups.all(): # si es lider y responsable entra como responsable
           return render_to_response('plan/responsable.html')
        ps = proyecto.objects.filter(responsable=request.user).filter(activo=True).order_by("id")
        return render_to_response('plan/lider.html', {'ol' : ps, 'bu' : burl }, context_instance=RequestContext(request))
    custgroup = Group.objects.get(name="responsable") 
    if custgroup in request.user.groups.all():
        ps = accion.objects.filter(responsable=request.user).filter(activo=True).order_by("id")
        return render_to_response('plan/responsable.html', {'ol' : ps, 'bu' : burl }, context_instance=RequestContext(request))
    custgroup = Group.objects.get(name="administrador") 
    if custgroup in request.user.groups.all():
        ps = [objetivo.objects.order_by("id"), meta.objects.order_by("id"), estrategia.objects.order_by("id"), proyecto.objects.order_by("id"), accion.objects.order_by("id")]
        return render_to_response('propuesta/admin.html', {'ol' : ps, 'bu' : burl }, context_instance=RequestContext(request))
    ps = "Su usuario no esta asignado a rol alguno, contactar al administrador"
    return render_to_response('plan/msg.html', {'ms' : ps, 'bu' : burl })

def objet(request, ob_id):
    ps = objetivo.objects.filter(pk=ob_id)
    custgroup = Group.objects.get(name="ejecutivo")
    if custgroup in request.user.groups.all():
        custgroup = Group.objects.get(name="manager") 
        if custgroup in request.user.groups.all():
           return render_to_response('plan/manager-objetivo.html', {'ob' : ps, 'bu' : burl }, context_instance=RequestContext(request))
        return render_to_response('plan/ejecutivo-objetivo.html', {'ob' : ps, 'bu' : burl }, context_instance=RequestContext(request))
    custgroup = Group.objects.get(name="manager")
    if custgroup in request.user.groups.all():
        return render_to_response('plan/manager-objetivo.html', {'ob' : ps, 'bu' : burl }, context_instance=RequestContext(request))
    return HttpResponse("ob_id")

def addo(request): # agrega un objetivo
   if request.method == 'POST':
      od = ObjetivoForm(request.POST, request.FILES)
      if od.is_valid():
         correo = persona.objects.get(pk=od.cleaned_data[0]['autor'])
         send_mail('Aviso del planeador', 'Se le acaba de asignar un objetivo.', 'rreyes@mora.edu.mx', [correo.email])
         od.save()
         return HttpResponseRedirect('../../')
      else:
         erro = ""
         for err in od.errors:
            erro += str(err)
         msg = "Se produjo un error (" + erro + ") al capturar los datos"
         return render_to_response('plan/msg.html', {'ms' : msg, 'bu' : burl }, context_instance=RequestContext(request))
   else:
      od = ObjetivoForm(queryset=objetivo.objects.none())
   return render_to_response('plan/objetivo_edit.html', {'of': od, 'bu' : burl }, context_instance=RequestContext(request) )   

@login_required(login_url = burl + "accounts/login/")
def edito(request, ob_id):
   if request.method == 'POST':
      od = ObjetivoForm(request.POST, request.FILES)
      if od.is_valid():
            # envio de correo en caso de problema
         od.save()
         return HttpResponseRedirect('../../../')
      else:
         msg = "Se produjo un error al capturar los datos:"
         return render_to_response('plan/msg.html', {'ms' : msg, 'er' : ad.errors, 'bu' : burl }, context_instance=RequestContext(request))
   else: 
      custgroup = Group.objects.get(name="ejecutivo")
      if custgroup in request.user.groups.all():
         ob = objetivo.objects.filter(pk=ob_id)
         od = ObjetivoForm(queryset=ob)
         return render_to_response('plan/objetivo_edit.html', {'of' : od, 'bu' : burl }, context_instance=RequestContext(request))
   return HttpResponse(ob_id)

def delo(request, ob_id):
    mensaje = "Se esta procediendo a borrar el objetivo: "
    mensaje += ob_id
    anterior = "../../../"
    borrado = burl+'objetivo/rmv/'
    borrado += ob_id
    borrado += '/'
    return render_to_response('plan/confirm.html', {'message' : mensaje, 'prev_link' : anterior, 'action_link' : borrado, 'bu' : burl }, context_instance=RequestContext(request))

@login_required(login_url = burl + "accounts/login/")
def delO(request, ob_id): # deshabilita
    ob = objetivo.objects.get(pk=ob_id)
    ob.activo = False
    ob.save()
    return HttpResponseRedirect('../../../')

#initial=[{'name': 'Some Name'},
#         {'name': 'Another Name'}])
@login_required(login_url = burl + "accounts/login/")
def adde(request):
   if request.method == 'POST':
      ed = EstrategiaForm(request.POST, request.FILES)
      if ed.is_valid():
#         correo = persona.objects.get(pk=ed.cleaned_data[0]['autor'])
#         send_mail('Aviso del planeador', 'Se le acaba de asignar una estrategia.', 'rreyes@mora.edu.mx', [correo.email])
         ed.save()
         return HttpResponseRedirect('../../')
      else:
         erro = ""
         for err in ed.errors:
            erro += str(err)
         msg = "Se produjo un error (" + erro + ") al capturar los datos"
         return render_to_response('plan/msg.html', {'ms' : msg, 'bu' : burl }, context_instance=RequestContext(request))
   else:
      ed = EstrategiaForm(queryset=estrategia.objects.none())
   return render_to_response('plan/estrategia_edit.html', {'ef': ed, 'bu' : burl }, context_instance=RequestContext(request) )   

@login_required(login_url = burl + "accounts/login/")
def edite(request, es_id):
   if request.method == 'POST':
      ed = EstrategiaForm(request.POST, request.FILES)
      if ed.is_valid():
         ed.save()
            # do something.
         return HttpResponseRedirect("../../..")
      else:
         erro = ""
         for err in ed.errors:
            erro += str(err)
         msg = "Se produjo un error (" + erro + ") al capturar los datos"
         return render_to_response('plan/msg.html', {'ms' : msg, 'bu' : burl }, context_instance=RequestContext(request))
   else:
      custgroup = Group.objects.get(name="manager")
      if custgroup in request.user.groups.all():
         est = estrategia.objects.filter(pk=es_id)
         ed = EstrategiaForm(queryset=est)
         hi = est[0].hijas()
         return render_to_response('plan/estrategia_edit.html', {'ei' : est[0], 'ef' : ed, 'eh' : hi, 'bu' : burl }, context_instance=RequestContext(request))
   return HttpResponse(es_id)

def dele(request, es_id):
    mensaje = "Se esta procediendo a borrar la estrategia: "
    mensaje += es_id
    anterior = "../../../"
    borrado = burl+"estrategia/rmv/"
    borrado += es_id
    borrado += "/"
    return render_to_response('plan/confirm.html', {'message' : mensaje, 'prev_link' : anterior, 'action_link' : borrado, 'bu' : burl }, context_instance=RequestContext(request))

@login_required(login_url = burl + "accounts/login/")
def delE(request, es_id):
    es = estrategia.objects.get(pk=es_id)
    #es.activo = False
    es.delete()
    return HttpResponseRedirect('../../../')

def addm(request):
   if request.method == 'POST':
      md = MetaForm(request.POST, request.FILES)
      if md.is_valid():
         correo = persona.objects.get(pk=md.cleaned_data[0]['autor'])
         send_mail('Aviso del planeador', 'Se le acaba de asignar una meta', 'rreyes@mora.edu.mx', [correo.email])
         md.save()
         return HttpResponseRedirect('../../')
      else:
         erro = ""
         for err in md.errors:
            erro += str(err)
         msg = "Se produjo un error (" + erro + ") al capturar los datos"
         return render_to_response('plan/msg.html', {'ms' : msg, 'bu' : burl }, context_instance=RequestContext(request))
   else:
      md = MetaForm(queryset=meta.objects.none())
   return render_to_response('plan/meta_edit.html', {'mf': md, 'bu' : burl }, context_instance=RequestContext(request) )   

@login_required(login_url = burl + "accounts/login/")
def editm(request, me_id):
   if request.method == 'POST':
      md = MetaForm(request.POST, request.FILES)
      if md.is_valid():
         md.save()
            # do something.
         return HttpResponseRedirect("../../..")
      else:
         erro = ""
         for err in md.errors:
            erro += str(err)
         msg = "Se produjo un error (" + erro + ") al capturar los datos"
         return render_to_response('plan/msg.html', {'ms' : msg, 'bu' : burl }, context_instance=RequestContext(request))
   else:
      custgroup = Group.objects.get(name="manager")
      if custgroup in request.user.groups.all():
         me = meta.objects.filter(pk=me_id)
         md = MetaForm(queryset=me)
         hi = me[0].hijas()
         return render_to_response('plan/meta_edit.html', {'mf' : md, 'mh' : hi, 'bu' : burl }, context_instance=RequestContext(request))
   return HttpResponse(me_id)

def delm(request, me_id):
    mensaje = "Se esta procediendo a borrar la meta: "
    mensaje += me_id
    anterior = "../../../"
    borrado = burl+"meta/rmv/"
    borrado += me_id
    borrado += "/"
    return render_to_response('plan/confirm.html', {'message' : mensaje, 'prev_link' : anterior, 'action_link' : borrado, 'bu' : burl }, context_instance=RequestContext(request))

@login_required(login_url = burl + "accounts/login/")
def delM(request, me_id):
    me = meta.objects.get(pk=me_id)
    #me.activo = False
    me.delete()
    return HttpResponseRedirect('../../../')

def addp(request):
   if request.method == 'POST':
      pd = ProyectoForm(request.POST, request.FILES)
      padre = request.POST['form-0-padre']
      if len(estrategia.objects.get(pk=padre).hijas()) > 4:
         msg = "Se produjo un error al capturar los datos:"
         error = "<p fontcolor=\"Red\"> Se rebasa el n&uacute;mero de proyectos</p>"
         return render_to_response('plan/msg.html', {'ms' : msg, 'er' : error, 'bu' : burl }, context_instance=RequestContext(request))
      if pd.is_valid() and len(estrategia.objects.get(pk=padre).hijas()) < 6:
         correo = persona.objects.get(pk=pd.cleaned_data[0]['responsable'])
         send_mail('Aviso del planeador', 'Se le acaba de asignar un proyecto.', 'rreyes@mora.edu.mx', [correo.email])
         pd.save()
         return HttpResponseRedirect('../../')
      else:
         msg = "Se produjo un error al capturar los datos:"
         return render_to_response('plan/msg.html', {'ms' : msg, 'er' : pd.errors, 'bu' : burl }, context_instance=RequestContext(request))
   else:
      pd = ProyectoForm(queryset=proyecto.objects.none())
      custgroup = Group.objects.get(name="manager")
      if custgroup in request.user.groups.all():
         return render_to_response('plan/proyecto_edit.html', {'pf': pd, 'mgr' : True, 'bu' : burl }, context_instance=RequestContext(request) )
   return render_to_response('plan/proyecto_edit.html', {'pf': pd, 'bu' : burl }, context_instance=RequestContext(request) )   

@login_required(login_url = burl + "accounts/login/")
def editp(request, pr_id):
   if request.method == 'POST':
      pd = ProyectoForm(request.POST, request.FILES)
      if pd.is_valid():
         pd.save()
            # do something.
         return HttpResponseRedirect("../../..")
      else:
         msg = "Se produjo un error al capturar los datos:"
         return render_to_response('plan/msg.html', {'ms' : msg, 'er' : pd.errors, 'bu' : burl }, context_instance=RequestContext(request))
   else:
      pro = proyecto.objects.filter(pk=pr_id)
      pd = ProyectoForm(queryset=pro)
      hi = pro[0].hijas()
      custgroup = Group.objects.get(name="manager")
      if custgroup in request.user.groups.all():
         return render_to_response('plan/proyecto_edit.html', {'pf' : pd, 'pi' : pro[0], 'mgr' : True, 'ph' : hi, 'bu' : burl }, context_instance=RequestContext(request))
      custgroup = Group.objects.get(name="lider")
      if custgroup in request.user.groups.all():
         return render_to_response('plan/proyecto_edit.html', {'pf' : pd, 'pi' : pro[0], 'ph' : hi, 'bu' : burl }, context_instance=RequestContext(request))
   return HttpResponse(pr_id)

def delp(request, pr_id):
    mensaje = "Se esta procediendo a borrar el proyecto: "
    mensaje += pr_id
    anterior = "../../../"
    borrado = burl+"proyecto/rmv/"
    borrado += pr_id
    borrado += "/"
    return render_to_response('plan/confirm.html', {'message' : mensaje, 'prev_link' : anterior, 'action_link' : borrado, 'bu' : burl }, context_instance=RequestContext(request))

@login_required(login_url = burl + "accounts/login/")
def delP(request, pr_id):
    pr = proyecto.objects.get(pk=pr_id)
    #pr.activo = False
    pr.delete()
    return HttpResponseRedirect('../../../')

def adda(request):
   if request.method == 'POST':
      ad = AccionForm(request.POST, request.FILES)
      padre = request.POST['form-0-padre']
      if len(proyecto.objects.get(pk=padre).hijas()) > 4:
         msg = "Se produjo un error al capturar los datos:"
         error = "<p fontcolor=\"Red\"> Se rebasa el n&uacute;mero de acciones</p>"
         return render_to_response('plan/msg.html', {'ms' : msg, 'er' : error, 'bu' : burl }, context_instance=RequestContext(request))
      elif ad.is_valid() and len(proyecto.objects.get(pk=padre).hijas()) < 6:
         correo = persona.objects.get(pk=ad.cleaned_data[0]['responsable'])
         send_mail('Aviso del planeador', 'Se le acaba de asignar una accion.', 'rreyes@mora.edu.mx', [correo.email])
         ad.save()
         return HttpResponseRedirect('../../')
      else:
         msg = "Se produjo un error al capturar los datos:"
         return render_to_response('plan/msg.html', {'ms' : msg, 'er' : ad.errors, 'bu' : burl }, context_instance=RequestContext(request))
   else:
      ad = AccionForm(queryset=accion.objects.none())
      custgroup = Group.objects.get(name="lider")
      if custgroup in request.user.groups.all():
         return render_to_response('plan/accion_edit.html', {'af': ad, 'lid' : True, 'bu' : burl }, context_instance=RequestContext(request) )
   return render_to_response('plan/accion_edit.html', {'af': ad, 'bu' : burl }, context_instance=RequestContext(request) )   

@login_required(login_url = burl + "accounts/login/")
def edita(request, ac_id):
   if request.method == 'POST':
      ad = AccionForm(request.POST, request.FILES)
      if ad.is_valid():
         send_mail('Aviso del planeador', 'Se acaba de actualizar a '+str(ad.cleaned_data[0]['avance'])+' el avance de la accion: '+str(ad.cleaned_data[0]['nombre'].encode('utf-8')), 'rreyes@mora.edu.mx', ['juan@goremo.mx'])
         ad.save()
         return HttpResponseRedirect("../../..")
      else:
         msg = "Se produjo un error al capturar los datos:"
         return render_to_response('plan/msg.html', {'ms' : msg, 'er' : ad.errors, 'bu' : burl }, context_instance=RequestContext(request))
   else:
      acc = accion.objects.filter(pk=ac_id)
      ad = AccionForm(queryset=acc)
      custgroup = Group.objects.get(name="lider")
      if custgroup in request.user.groups.all():
         return render_to_response('plan/accion_edit.html', {'af' : ad, 'lid' : True, 'prob' : acc[0].prob, 'bu' : burl }, context_instance=RequestContext(request))
      custgroup = Group.objects.get(name="responsable")
      if custgroup in request.user.groups.all():
         return render_to_response('plan/accion_edit.html', {'af' : ad, 'ai': acc[0], 'bu' : burl }, context_instance=RequestContext(request))
   return HttpResponse(ac_id)

def dela(request, ac_id):
    mensaje = "Se esta procediendo a borrar la accion: "
    mensaje += ac_id
    anterior = "../../../"
    borrado = burl+"accion/rmv/"
    borrado += ac_id
    borrado += "/"
    return render_to_response('plan/confirm.html', {'message' : mensaje, 'prev_link' : anterior, 'action_link' : borrado, 'bu' : burl }, context_instance=RequestContext(request))

@login_required(login_url = burl + "accounts/login/")
def delA(request, ac_id):
    ac = accion.objects.get(pk=ac_id)
    #ac.activo = False
    ac.delete()
    return HttpResponseRedirect('../../../')

@login_required(login_url = burl + "accounts/login/")
def addpr(request, pid, elem):
   if request.method == 'POST':
      prf = ProblemaForm(request.POST)
      if prf.is_valid():
         nuevo = prf[0].save()
         if elem == "proy":
            objeto = proyecto.objects.get(pk=pid)
         elif elem == "acci":
            objeto = accion.objects.get(pk=pid)
         elif elem == "estr":
            objeto = estrategia.objects.get(pk=pid)
         objeto.prob = nuevo
         objeto.save()
         return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                                (escape(nuevo._get_pk_val()), escape(nuevo)))
      else:
         msg = "Se produjo un error al capturar los datos:"
         return render_to_response('plan/msg.html', {'ms' : msg, 'er' : prf.errors, 'bu' : burl }, context_instance=RequestContext(request))
      return HttpResponseRedirect('javascript:javascript:history.go(-2)')
   else:
      pf = ProblemaForm(queryset=persona.objects.none())
      return render_to_response('plan/problema.html', {'prf': pf, 'bu' : burl, 'autor' : request.user, 'fecha': datetime.date.today()}, context_instance=RequestContext(request) )

@login_required(login_url = burl + "accounts/login/")
def editpr(request, pro_id, elem, a_id):
   if request.method == 'POST':
      prd = ProblemaForm(request.POST, request.FILES)
      if prd.is_valid():
         nuevo = prd[0].save()
            # do something.
         if elem == "proy":
            elemento = "proyecto"
         elif elem == "acci":
            objeto = accion.objects.get(pk=a_id)
         return HttpResponseRedirect(burl+'accion/edit/'+a_id+'/')
      else:
         msg = "Se produjo un error al capturar los datos:"
         return render_to_response('plan/msg.html', {'ms' : msg, 'er' : prd.errors, 'bu' : burl }, context_instance=RequestContext(request))
   else:
      prob = problema.objects.filter(pk=pro_id)
      prd = ProblemaForm(queryset=prob)
      return render_to_response('plan/problema.html', {'prf' : prd, 'pi' : prob[0], 'bu' : burl }, context_instance=RequestContext(request))
   
@login_required(login_url = burl + "accounts/login/")
def coment(request):
   if request.method == 'POST':
      prf = ComentProForm(request.POST)
      if prf.is_valid():
         nuevo = prf[0].save()
         return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                                (escape(nuevo._get_pk_val()), escape(nuevo)))
      else:
         msg = "Se produjo un error al capturar los datos:"
         return render_to_response('plan/msg.html', {'ms' : msg, 'er' : prf.errors, 'bu' : burl }, context_instance=RequestContext(request))
      return HttpResponseRedirect('javascript:javascript:history.go(-2)')
   else:
      pf = ProblemaForm(queryset=persona.objects.none())
      return render_to_response('plan/problema.html', {'prf': pf, 'bu' : burl, 'autor' : request.user, 'fecha': datetime.date.today()}, context_instance=RequestContext(request) )

@login_required(login_url = burl + "accounts/login/")
def pers(request):
    if request.method == 'POST':
       pf = PersonaForm(request.POST)
       raw_p = pf.cleaned_data[0]['password']
       if pf.is_valid():
          Persona = pf[0].save()
          nuevo = persona.objects.get(pk=Persona.pk)
          nuevo.password = 'sha1$'+'gorem$'+get_hex('sha1', 'gorem', raw_p)
          if Group.objects.get(name='ejecutivo') in request.user.groups.all() and Persona:
             nuevo.groups.add(Group.objects.get(name='manager'))
             nuevo.is_active = True
             nuevo.save()
             return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                                    (escape(nuevo._get_pk_val()), escape(nuevo)))
          if Group.objects.get(name='manager') in request.user.groups.all() and Persona:
             nuevo.groups.add(Group.objects.get(name='lider'))
             nuevo.is_active = True
             nuevo.save()
             return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                                    (escape(nuevo._get_pk_val()), escape(nuevo)))
          if Group.objects.get(name='lider') in request.user.groups.all() and Persona:
             nuevo.groups.add(Group.objects.get(name='responsable'))
             nuevo.is_active = True
             nuevo.save()
             return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                                    (escape(nuevo._get_pk_val()), escape(nuevo)))
          else: 
             msg = "Usted no puede agregar usuarios al sistema"
             return render_to_response('plan/msg.html', {'ms' : msg, 'bu' : burl }, context_instance=RequestContext(request))
       else:
          msg = "Se produjo un error al capturar los datos:"
          return render_to_response('plan/msg.html', {'ms' : msg, 'er' : pf.errors, 'bu' : burl }, context_instance=RequestContext(request))
       return HttpResponseRedirect('javascript:javascript:history.go(-2)')
    else:
       pf = PersonaForm(queryset=persona.objects.none())
       return render_to_response('plan/persona.html', {'Pf': pf, 'bu' : burl }, context_instance=RequestContext(request) )

@login_required(login_url = burl + "accounts/login/")
def obj(request):
    r = "Impresion general<br><a href=\"javascript:window.print()\">Imprimir</a><br><a href=\"javascript:javascript:history.go(-1)\">Regresar</a><ul>"
    ol = objetivo.objects.order_by("id")
    for o in ol:
        if not o.activo:
           r += "<i>"
        r += "<li>Objetivo %s: %s (%s)"%(o.id,o.nombre,o.autor.get_full_name())
        r += "<ul>"
        for mh in o.hijas():
	    mo = meta.objects.get(pk=mh.id)
            if not mo.activo:
               r += "<i>"
            r += "<li>Meta %s.%s: %s (%s)" %(o.id,mo.id,mo.nombre,mo.fecha)
            r += "<ul>"
            for eh in mo.hijas():
               eo = estrategia.objects.get(pk=eh.id)
               if not eo.activo:
                  r += "<i>"
               r += "<li>Estrategia %s.%s.%s: %s (%s)" %(o.id,mo.id,eo.id,eo.nombre,eo.semaforo())
               r += "<ul>"
               for ph in eo.hijas():
                  po = proyecto.objects.get(pk=ph.id)
                  if not po.activo:
                     r += "<i>"
                  r += "<li>Proyecto %s.%s.%s.%s: %s (%s)" %(o.id,mo.id,eo.id,po.id,po.nombre,po.responsable.get_full_name())
                  r += "<ul>"
                  for ah in po.hijas():
                     ao = accion.objects.get(pk=ah.id)
                     if not ao.activo:
                        r += "<i>"
                     r += "<li>Accion %s.%s.%s.%s.%s: %s (%s, %s, %s)</li>" %(o.id,mo.id,eo.id,po.id,ao.id,ao.nombre,ao.responsable.get_full_name(),ao.fecha,ao.avance)
                     if not ao.activo:
                        r += "</i>"
                  r += "</ul></li>"
                  if not po.activo:
                     r += "</i>"
               r += "</ul></li>"
               if not eo.activo:
                  r += "</i>"
            r += "</ul></li>"
            if not mo.activo:
               r += "</i>"
        r += "</ul></li>"
        if not o.activo:
           r += "</i>"
    r += "</ul>"
    return HttpResponse(r)

def met(request):
    r = "Lista de Metas<ul>"
    ml = meta.objects.order_by("id")
    for m in ml:
	r += "<li>%s: " %(m.nombre)
        for eh in m.hijas():
	    eo = estrategia.objects.filter(pk=eh.id)
	    for eid in eo:
		r += "<th scope=\"row\"><a href=\"/goremo/admin/captura/estrategia/%s/\">%s</a></th> " %(eid.id,eid.nombre)
        r += "</li>"
    r += "</ul>"
    return HttpResponse(r)

def est(request):
    r = "Lista de Estrategias<ul>"
    el = estrategia.objects.order_by("id")
    for e in el:
	r += "<li>%s: " %(e.nombre)
        for ph in e.hijas():
	    po = proyecto.objects.filter(pk=ph.id)
	    for pid in po:
		r += "<th scope=\"row\"><a href=\"/goremo/admin/captura/proyecto/%s/\">%s</a></th> " %(pid.id,pid.nombre)
        r += "</li>"
    r += "</ul>"
    return HttpResponse(r)

def pro(request):
    r = "Lista de Proyectos<ul>"
    pl = proyecto.objects.order_by("id")
    for p in pl:
	r += "<li>%s: " %(p.nombre)
        for ah in p.hijas():
	    ao = accion.objects.filter(pk=ah.id)
	    for aid in ao:
		r += "<th scope=\"row\"><a href=\"/goremo/admin/captura/accion/%s/\">%s</a></th> " %(aid.id,aid.nombre)
        r += "</li>"
    r += "</ul>"
    return HttpResponse(r)

def acc(request):
    r = "Lista de Acciones<ul>"
    al = accion.objects.order_by("id")
    for a in al:
	r += "<li>%s: " %(a.nombre)
        r += "</li>"
    r += "</ul>"
    return HttpResponse(r)

def opt(request):
    custgroup = Group.objects.get(name="manager") 
    if custgroup in request.user.groups.all():
        ps = ['objetivo', 'meta', 'estrategia', 'proyecto']
        return render_to_response('plan/opciones.html', {'op' : ps})
    ps = ['accion']
    return render_to_response('plan/opciones.html', {'op' : ps})

def objetivo_edit(request, objetivo_id):
    Objetivo = objetivo.objects.get(pk=objetivo_id)
    form = objetivoFrom(request.POST or None, instance=Objetivo)
    if form.is_valid():
        Objetivo = form.save()
        #this is where you might choose to do stuff like send e-mail.
        #contact.name = 'test'
        Objetivo.save()
        return redirect(obj)
    return render_to_response('captura/objetivo_edit.html',
                              {'objetivo_form': form,
                               'objetivo_id': objetivo_id},
                              context_instance=RequestContext(request))

def meta_edit(request, meta_id):
    Meta = meta.objects.get(pk=meta_id)
    form = metaForm(request.POST or None, instance=Meta)
    if form.is_valid():
        Meta = form.save()
        #this is where you might choose to do stuff like send e-mail.
        #contact.name = 'test'
        Meta.save()
        return redirect(obj)
    return render_to_response('captura/meta_edit.html',
                              {'meta_form': form,
                               'meta_id': meta_id},
                              context_instance=RequestContext(request))

def estrategia_edit(request, estrategia_id):
    Estrategia = estrategia.objects.get(pk=estrategia_id)
    form = estrategiaForm(request.POST or None, instance=Estrategia)
#    estrategia_pro = Estrategiainline(request.POST, instance=Estrategia)
    if form.is_valid():
        Estrategia = form.save(commit=False)
        #this is where you might choose to do stuff like send e-mail.
        #contact.name = 'test'
        Estrategia.save()
        return redirect(obj)
    return render_to_response('captura/estrategia_edit.html',
                              {'estrategia_form': form,
#                               'estrategia_pro': estrategia_pro,
                               'estrategia_id': estrategia_id},
                              context_instance=RequestContext(request))

def proyecto_edit(request, proyecto_id):
    Proyecto = proyecto.objects.get(pk=proyecto_id)
    form = proyectoForm(request.POST or None, instance=Proyecto)
#    proyecto_pro = Proyectoinline(request.POST, instance=Proyecto)
    if form.is_valid():
        Proyecto = form.save(commit=False)
        #this is where you might choose to do stuff like send e-mail.
        #contact.name = 'test'
        Proyecto.save()
        return redirect(obj)
    return render_to_response('captura/proyecto_edit.html',
                              {'proyecto_form': form,
#                               'proyecto_pro': proyecto_pro,
                               'proyecto_id': proyecto_id},
                              context_instance=RequestContext(request))

def accion_edit(request, accion_id):
    Accion = accion.objects.get(pk=accion_id)
    form = accionForm(request.POST or None, instance=Accion)
#    form = accionFormSet(queryset=accion.objects.filter(pk=accion_id))
    accion_pro = Accioninline(instance=Accion)
    if form.is_valid():
        Accion = form.save(commit=False)
        accion_pro = Accioninline(request.POST, instance=Accion)
        #this is where you might choose to do stuff like send e-mail.
        #contact.name = 'test'
        Accion.save()
        return redirect(obj)
    return render_to_response('captura/accion_edit.html',
                              {'accion_form': accion_pro,
                               'accion_pro': form,
                               'accion_id': accion_id},
                              context_instance=RequestContext(request))

def adm(request):
    forma = Accioninline()
#    forma = accionForm(request.POST, request.FILES)
    return render_to_response('plan/form.html', {'formset' : forma}, context_instance=RequestContext(request))

