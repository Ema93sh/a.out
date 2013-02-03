from apps.practice.views import *

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'online_judge.views.home', name='home'),
    url(r'logout$', 'online_judge.views.logoutView'),
    url(r'^account/',include('apps.account.urls')),
    url(r'^practice/', include('apps.practice.urls' )), 
    url(r'^contest/', include('apps.contest.urls')),
    url(r'^submission/', include('apps.submission.urls')),
    url(r'^author/', include('apps.author.urls')),

    
    #    url(r'^tinymce/', include('apps.tinymce.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    url(r'^admin/', include(admin.site.urls)),
)
