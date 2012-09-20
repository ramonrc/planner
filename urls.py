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
    url(r'^captura/', include('captura.urls')),
    #url(r'^polls/', include('polls.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^seguimiento/', include('seguimiento.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

#if settings.DEBUG:
#urlpatterns += patterns('',
#    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
#        'document_root': settings.STATIC_ROOT,
#    }),
# )
