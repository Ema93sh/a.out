from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()

urlpatterns = patterns('',
		url(r'$','apps.account.views.registerUser'),		   
		)
