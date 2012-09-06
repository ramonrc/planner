# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.template import RequestContext
from models import *

@login_required(login_url='/goremo/accounts/login/')
def lista(request):
    custgroup = Group.objects.get(name="ejecutivo") 
#    if custgroup not in request.user.groups.all():
#        return HttpResponse("Usted no puede ver esta lista")
    ps = [objetivo.objects.order_by("id"), meta.objects.order_by("id"), estrategia.objects.order_by("id"), proyecto.objects.order_by("id"), accion.objects.order_by("id")]
    return render_to_response('plan/listas.html', {'ol' : ps})

def opt(request):
    ps = ['objetivo', 'meta', 'estrategia', 'proyecto', 'accion']
    return render_to_response('plan/opciones.html', {'op' : ps})

def obj(request):
    r = "Lista de Objetivos<ul>"
    ol = objetivo.objects.order_by("id")
    for o in ol:
        r += "<li>%s: " %(o.nombre)
        for mh in o.hijas():
	    mo = meta.objects.filter(pk=mh)
	    for mid in mo:
                r += "<th scope=\"row\"><a href=\"/goremo/admin/captura/meta/%s/\">%s</a></th> " %(mid.id,mid.nombre)
        r += "</li>"
    r += "</ul>"
    return HttpResponse(r)

def met(request):
    r = "Lista de Metas<ul>"
    ml = meta.objects.order_by("id")
    for m in ml:
	r += "<li>%s: " %(m.nombre)
        for eh in m.hijas():
	    eo = estrategia.objects.filter(pk=eh)
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
	    po = proyecto.objects.filter(pk=ph)
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
	    ao = accion.objects.filter(pk=ah)
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
        #this is where you might choose to do stuff.
        #contact.name = 'test'
        Objetivo.save()
        return redirect(obj)

    return render_to_response('captura/objetivo_edit.html',
                              {'objetivo_form': form,
                               'objetivo_id': objetivo_id},
                              context_instance=RequestContext(request))

