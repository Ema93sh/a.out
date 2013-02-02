from django.contrib import admin
from django.conf.urls import patterns, include, url
from views import *
admin.autodiscover()

urlpatterns = patterns('',
               url(r'login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
               url(r'(?P<user_name>[A-Za-z0-9-]+)/edit/$', 'apps.account.views.editprofile'),
               url(r'(?P<user_name>[A-Za-z0-9-]+)/$', 'apps.account.views.profile'),
		)
