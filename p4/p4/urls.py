from django.conf.urls import patterns, include, url

from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from p4 import settings

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from p4app import views

urlpatterns = patterns('',
    url(r'^$', 'p4app.views.index', name='index'),
    url(r'^compiler$', 'p4app.views.compiler', name='compiler'),
    url(r'^debugger$', 'p4app.views.debugger', name='debugger'),
    url(r'^debuggerBreak$', 'p4app.views.debuggerBreak', name='debuggerBreak'),
    url(r'^debuggerPrint$', 'p4app.views.debuggerPrint', name='debuggerPrint'),
    url(r'^debuggerClear$', 'p4app.views.debuggerClear', name='debuggerClear'),
    
    # Examples:
    # url(r'^$', 'p4.views.home', name='home'),
    # url(r'^p3/', include('p4.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
