from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from captura.models import *

urlpatterns = patterns('',
        (r'^proyecto/$', 'pro')
)
