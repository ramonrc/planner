from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from captura.models import objetivo

obj_dict = {
    'queryset': objetivo.objects.all(),
}

urlpatterns = patterns('',
    (r'^objetivos/$', 'django.views.generic.list_detail.object_list', obj_dict),
    url(r'^obj/$', ListView.as_view( queryset=objetivo.objects.all(), context_object_name='op', template_name='plan/listas.html')))

urlpatterns += patterns('captura.views',
    url(r'^$', 'opt'),
    url(r'^objetivo/$', 'obj'),
    url(r'^meta/$', 'met'),
    url(r'^estrategia/$', 'est'),
    url(r'^proyecto/$', 'pro'),
    url(r'^objetivo_edit/(?P<objetivo_id>\d+)/$', 'objetivo_edit'),
    url(r'^meta_edit/(?P<meta_id>\d+)/$', 'meta_edit'),
    url(r'^estrategia_edit/(?P<estrategia_id>\d+)/$', 'estrategia_edit'),
    url(r'^proyecto_edit/(?P<proyecto_id>\d+)/$', 'proyecto_edit'),
    url(r'^accion_edit/(?P<accion_id>\d+)/$', 'accion_edit'),
)

