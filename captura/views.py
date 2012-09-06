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
    if custgroup in request.user.groups.all():
        ps = [objetivo.objects.order_by("id"), meta.objects.order_by("id"), estrategia.objects.order_by("id"), proyecto.objects.order_by("id"), accion.objects.order_by("id")]
        return render_to_response('plan/listas.html', {'ol' : ps})
    ps = objetivo.objects.filter(autor=request.user)
    return render_to_response('plan/panel.html', {'ol' : ps})

def opt(request):
    custgroup = Group.objects.get(name="manager") 
    if custgroup in request.user.groups.all():
        ps = ['objetivo', 'meta', 'estrategia', 'proyecto']
        return render_to_response('plan/opciones.html', {'op' : ps})
    ps = ['accion']
    return render_to_response('plan/opciones.html', {'op' : ps})

def obj(request):
    r = "Lista de Objetivos<ul>"
    ol = objetivo.objects.order_by("id")
    for o in ol:
        r += "<li>%s: " %(o.nombre)
        for mh in o.hijas():
	    mo = meta.objects.filter(pk=mh.id)
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

