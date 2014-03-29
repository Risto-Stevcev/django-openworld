from django.conf.urls import patterns, url
from openworld import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^login/$', 'django.contrib.auth.views.login', {
        'template_name': 'openworld/login.html'
    }, name='login'),
    url(r'^info/$', views.user_info, name='info'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^viewentries/$', views.view_entries, name='viewentries'),
    url(r'^viewentry/(?P<entry_id>\d+)/$', views.view_entry, name='viewentry'),
    url(r'^taggedentries/$', views.tagged_entries, name='taggedentries'),
    url(r'^submitnewrequest/$', views.submit_new_request, name='submitnewrequest'),
    url(r'^submitrequest/$', views.submit_request, name='submitrequest'),
    url(r'^submittags/$', views.submit_tags, name='submittags'),
    url(r'^tagsform/(?P<entry_id>\d+)/$', views.tags_form, name='tagsform'),
    url(r'^viewrequests/$', views.view_requests, name='viewrequests'),
    url(r'^register/$', views.register, name='register'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
)
