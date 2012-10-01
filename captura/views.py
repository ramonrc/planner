# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from django.template import RequestContext
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
        custgroup2 = Group.objects.get(name="manager") 
        ps = objetivo.objects.filter(activo=True).order_by("id")
        if custgroup2 in request.user.groups.all(): # si es manageer y ejecutivo entra como manager
           return render_to_response('plan/manager.html', {'ol' : ps, 'bu' : burl }, context_instance=RequestContext(request))
        return render_to_response('plan/ejecutivo.html', {'ol' : ps, 'bu' : burl }, context_instance=RequestContext(request))
    custgroup = Group.objects.get(name="manager") 
    if custgroup in request.user.groups.all():
        ps = objetivo.objects.filter(autor=request.user).filter(activo=True).order_by("id")
        return render_to_response('plan/manager.html', {'ol' : ps, 'bu' : burl }, context_instance=RequestContext(request))
    custgroup = Group.objects.get(name="lider") 
    if custgroup in request.user.groups.all():
        custgroup2 = Group.objects.get(name="responsable")
        if custgroup2 in request.user.groups.all():
           return render_to_response('plan/lider.html')
        ps = proyecto.objects.filter(responsable=request.user).filter(activo=True).order_by("id")
        return render_to_response('propuesta/seguimiento-proyecto.html', {'ol' : ps, 'bu' : burl }, context_instance=RequestContext(request))
    custgroup = Group.objects.get(name="responsable") 
    if custgroup in request.user.groups.all():
        ps = accion.objects.filter(responsable=request.user).filter(activo=True).order_by("id")
        return render_to_response('propuesta/seguimiento-accion.html', {'ol' : ps, 'bu' : burl }, context_instance=RequestContext(request))
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
        custgroup2 = Group.objects.get(name="manager") 
        if custgroup2 in request.user.groups.all():
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
            # envio de correo a el manager responsabla
         od.save()
         return HttpResponseRedirect('../../')
      else:
         msg = "Se produjo un error al capturar los datos"
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
         msg = "Se produjo un error al capturar los datos"
         return render_to_response('plan/msg.html', {'ms' : msg, 'bu' : burl }, context_instance=RequestContext(request))
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

def adde(request):
   if request.method == 'POST':
      ed = EstrategiaForm(request.POST, request.FILES)
      if ed.is_valid():
         ed.save()
         return HttpResponseRedirect('../../')
      else:
         msg = "Se produjo un error al capturar los datos"
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
         msg = "Se produjo un error al capturar los datos"
         return render_to_response('plan/msg.html', {'ms' : msg, 'bu' : burl }, context_instance=RequestContext(request))
   else:
      custgroup = Group.objects.get(name="manager")
      if custgroup in request.user.groups.all():
         est = estrategia.objects.get(pk=es_id)
         ed = [ estrategiaForm(instance=est) ]
         hi = est.hijas()
         return render_to_response('plan/estrategia_edit.html', {'ei' : est, 'ef' : ed, 'eh' : hi, 'bu' : burl }, context_instance=RequestContext(request))
   return HttpResponse(es_id)

def dele(request, es_id):
    mensaje = "Se esta procediendo a borrar la estrategia: "
    mensaje =+ es_id
    anterior = "../../../"
    borrado = burl+"estrategia/rmv/"
    borrado += es_id
    borrado += "/"
    return render_to_response('plan/confirm.html', {'message' : mensaje, 'prev_link' : anterior, 'action_link' : borrado, 'bu' : burl }, context_instance=RequestContext(request))

@login_required(login_url = burl + "accounts/login/")
def delE(request, es_id):
    es = estrategia.objects.get(pk=es_id)
#    es.activo = False
    es.save()
    return HttpResponseRedirect('../../../')

def addm(request):
   if request.method == 'POST':
      md = MetaForm(request.POST, request.FILES)
      if md.is_valid():
         md.save()
         return HttpResponseRedirect('../../')
      else:
         msg = "Se produjo un error al capturar los datos"
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
         msg = "Se produjo un error al capturar los datos"
         return render_to_response('plan/msg.html', {'ms' : msg, 'bu' : burl }, context_instance=RequestContext(request))
   else:
      custgroup = Group.objects.get(name="manager")
      if custgroup in request.user.groups.all():
         me = meta.objects.filter(pk=me_id)
         met = meta.objects.get(pk=me_id)
         md = MetaForm(queryset=me)
         hi = met.hijas()
         return render_to_response('plan/meta_edit.html', {'mf' : md, 'mh' : hi, 'bu' : burl }, context_instance=RequestContext(request))
   return HttpResponse(me_id)

def delm(request, me_id):
    mensaje = "Se esta procediendo a borrar la meta: "
    mensaje =+ me_id
    anterior = "../../../"
    borrado = burl+"estrategia/rmv/"
    borrado += me_id
    borrado += "/"
    return render_to_response('plan/confirm.html', {'message' : mensaje, 'prev_link' : anterior, 'action_link' : borrado, 'bu' : burl }, context_instance=RequestContext(request))

@login_required(login_url = burl + "accounts/login/")
def delM(request, me_id):
    me = estrategia.objects.get(pk=me_id)
#    me.activo = False
    me.save()
    return HttpResponseRedirect('../../../')

def addp(request):
   if request.method == 'POST':
      pd = ProyectoForm(request.POST, request.FILES)
      if pd.is_valid():
         pd.save()
         return HttpResponseRedirect('../../')
      else:
         msg = "Se produjo un error al capturar los datos"
         return render_to_response('plan/msg.html', {'ms' : msg, 'bu' : burl }, context_instance=RequestContext(request))
   else:
      pd = ProyectoForm(queryset=proyecto.objects.none())
   return render_to_response('plan/proyecto_edit.html', {'pf': pd, 'bu' : burl }, context_instance=RequestContext(request) )   

def delp(request, pr_id):
    mensaje = "Se esta procediendo a borrar la estrategia: "
    mensaje =+ pr_id
    anterior = "../../../"
    borrado = burl+"estrategia/rmv/"
    borrado += pr_id
    borrado += "/"
    return render_to_response('plan/confirm.html', {'message' : mensaje, 'prev_link' : anterior, 'action_link' : borrado, 'bu' : burl }, context_instance=RequestContext(request))

@login_required(login_url = burl + "accounts/login/")
def delP(request, pr_id):
    pr = proyecto.objects.get(pk=pr_id)
    pr.activo = False
    pr.save()
    return HttpResponseRedirect('../../../')

def adda(request):
   if request.method == 'POST':
      ad = AccionForm(request.POST, request.FILES)
      if ad.is_valid():
         ad.save()
         return HttpResponseRedirect('../../')
      else:
         msg = "Se produjo un error al capturar los datos"
         return render_to_response('plan/msg.html', {'ms' : msg, 'bu' : burl }, context_instance=RequestContext(request))
   else:
      ad = MetaForm(queryset=accion.objects.none())
   return render_to_response('plan/accion_edit.html', {'af': ad, 'bu' : burl }, context_instance=RequestContext(request) )   

def dela(request, ac_id):
    mensaje = "Se esta procediendo a borrar la estrategia: "
    mensaje =+ ac_id
    anterior = "../../../"
    borrado = burl+"estrategia/rmv/"
    borrado += ac_id
    borrado += "/"
    return render_to_response('plan/confirm.html', {'message' : mensaje, 'prev_link' : anterior, 'action_link' : borrado, 'bu' : burl }, context_instance=RequestContext(request))

@login_required(login_url = burl + "accounts/login/")
def delA(request, ac_id):
    ac = proyecto.objects.get(pk=ac_id)
    ac.activo = False
    ac.save()
    return HttpResponseRedirect('../../../')

def opt(request):
    custgroup = Group.objects.get(name="manager") 
    if custgroup in request.user.groups.all():
        ps = ['objetivo', 'meta', 'estrategia', 'proyecto']
        return render_to_response('plan/opciones.html', {'op' : ps})
    ps = ['accion']
    return render_to_response('plan/opciones.html', {'op' : ps})

@login_required(login_url = burl + "accounts/login/")
def obj(request):
    r = "Impresion general<br><a href=\"javascript:window.print()\">Imprimir</a><br><a href=\"javascript:javascript:history.go(-1)\">Regresar</a><ul>"
    ol = objetivo.objects.order_by("id")
    for o in ol:
        if not o.activo:
           r += "<i>"
        r += "<li>Objetivo %s: %s "%(o.id,o.nombre)
        r += "<ul>"
        for mh in o.hijas():
	    mo = meta.objects.get(pk=mh.id)
            if not mo.activo:
               r += "<i>"
            r += "<li>Meta %s.%s: %s " %(o.id,mo.id,mo.nombre)
            r += "<ul>"
            for eh in mo.hijas():
               eo = estrategia.objects.get(pk=eh.id)
#               if not eo.activo:
#                  r += "<i>"
               r += "<li>Estrategia %s.%s.%s: %s " %(o.id,mo.id,eo.id,eo.nombre)
               r += "<ul>"
               for ph in eo.hijas():
                  po = proyecto.objects.get(pk=ph.id)
                  if not po.activo:
                     r += "<i>"
                  r += "<li>Proyecto %s.%s.%s.%s: %s " %(o.id,mo.id,eo.id,po.id,po.nombre)
                  r += "<ul>"
                  for ah in po.hijas():
                     ao = accion.objects.get(pk=ah.id)
                     if not ao.activo:
                        r += "<i>"
                     r += "<li>Accion %s.%s.%s.%s.%s: %s </li>" %(o.id,mo.id,eo.id,po.id,ao.id,ao.nombre)
                     if not ao.activo:
                        r += "</i>"
                  r += "</ul></li>"
                  if not po.activo:
                     r += "<i>"
               r += "</ul></li>"
#               if not eo.activo:
#                  r += "<i>"
            r += "</ul></li>"
            if not mo.activo:
               r += "<i>"
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

def adm(request):
#    forma = Accioninline()
#    forma = accionForm(request.POST, request.FILES)
    
    return render_to_response('plan/form.html', {'formset' : forma}, context_instance=RequestContext(request))

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

