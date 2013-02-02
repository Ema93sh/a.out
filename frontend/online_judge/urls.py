from apps.practice.views import *

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'online_judge.views.home', name='home'),
    url(r'^account/logout$', 'online_judge.views.logoutView'),
    url(r'^account/login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^account/(?P<user_name>[A-Za-z0-9-]+)/edit/$', 'online_judge.views.editprofile'),
    url(r'^account/(?P<user_name>[A-Za-z0-9-]+)/$', 'online_judge.views.profile'),
    url(r'^practice/', include('apps.practice.urls' )), 
    url(r'^contest/', include('apps.contest.urls')),
    url(r'^submission/', include('apps.submission.urls')),
    url(r'^author/', include('apps.author.urls')),
    url(r'^register/', include('apps.account.urls')),

    
    #    url(r'^tinymce/', include('apps.tinymce.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    url(r'^admin/', include(admin.site.urls)),
)
