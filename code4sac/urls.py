from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'code4sac.views.home', name='home'),
    url(r'^openworld/', include('openworld.urls', namespace='openworld')),
    url(r'^accounts/profile/$', 'openworld.views.dashboard', name='dashboard'),
    url(r'^accounts/login/$', 
       'django.contrib.auth.views.login', {
    'template_name': 'openworld/login.html'
    }), 
        
    url(r'^admin/', include(admin.site.urls)),
)
