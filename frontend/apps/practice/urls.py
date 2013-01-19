from views import *

from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()

urlpatterns = patterns('',
		   url(r'^$', problemListView.as_view() ),
		   url(r'^problem/(?P<slug>[a-zA-Z0-9]+)/$',  problemDetailView.as_view()),
		   url(r'^problem/(?P<problem_code>[a-zA-Z0-9]+)/submit/$', 'apps.practice.views.submit'),
		   url(r'^problem/(?P<problem_code>[a-zA-z0-9]+)/comment/add$', 'apps.practice.views.addComment'),
		   )
