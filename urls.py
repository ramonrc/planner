from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'goremo.views.home', name='home'),
    # url(r'^goremo/', include('goremo.foo.urls')),
    url(r'^$', 'captura.views.lista'),
    url(r'^captura/', include('captura.urls')),
    #url(r'^polls/', include('polls.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^seguimiento/', include('seguimiento.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
