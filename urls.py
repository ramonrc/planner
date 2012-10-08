from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'goremo.views.home', name='home'),
    # url(r'^goremo/', include('goremo.foo.urls')),
    url(r'^$', 'captura.views.inicio'),
    url(r'^objetivo/view/(?P<ob_id>\d+)/$', 'captura.views.objet'),
    url(r'^objetivo/edit/(?P<ob_id>\d+)/$', 'captura.views.edito'),
    url(r'^objetivo/add/', 'captura.views.addo'),
    url(r'^objetivo/rm/(?P<ob_id>\d+)/$', 'captura.views.delo'),
    url(r'^objetivo/rmv/(?P<ob_id>\d+)/$', 'captura.views.delO'),
    url(r'^meta/edit/(?P<me_id>\d+)/$', 'captura.views.editm'),
    url(r'^meta/add/', 'captura.views.addm'),
    url(r'^meta/rm/(?P<me_id>\d+)/$', 'captura.views.delm'),
    url(r'^meta/rmv/(?P<me_id>\d+)/$', 'captura.views.delM'),
    url(r'^estrategia/edit/(?P<es_id>\d+)/$', 'captura.views.edite'),
    url(r'^estrategia/add/', 'captura.views.adde'),
    url(r'^estrategia/rm/(?P<es_id>\d+)/$', 'captura.views.dele'),
    url(r'^estrategia/rmv/(?P<es_id>\d+)/$', 'captura.views.delE'),
    url(r'^proyecto/edit/(?P<pr_id>\d+)/$', 'captura.views.editp'),
    url(r'^proyecto/add/', 'captura.views.addp'),
    url(r'^proyecto/rm/(?P<pr_id>\d+)/$', 'captura.views.delp'),
    url(r'^proyecto/rmv/(?P<pr_id>\d+)/$', 'captura.views.delP'),
    url(r'^accion/edit/(?P<ac_id>\d+)/$', 'captura.views.edita'),
    url(r'^accion/add/', 'captura.views.adda'),
    url(r'^accion/rm/(?P<ac_id>\d+)/$', 'captura.views.dela'),
    url(r'^accion/rmv/(?P<ac_id>\d+)/$', 'captura.views.delA'),
    url(r'^accion/$', 'captura.views.adm'),
    url(r'^logout/$', 'captura.views.logout_page'),
    url(r'^impresion/$', 'captura.views.obj'),
    #url(r'^captura/', include('captura.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    #url(r'^seguimiento/', include('seguimiento.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
