from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()

urlpatterns = patterns('',
		url(r'^problem/$', 'apps.author.views.authorProblemsView'),
		url(r'^problem/add$', 'apps.author.views.addProblem'),
		url(r'^problem/edit/(?P<problem_code>[A-Za-z]+)/$', 'apps.author.views.editProblem'),		   
		)
