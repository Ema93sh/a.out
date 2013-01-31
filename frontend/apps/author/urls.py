from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()

urlpatterns = patterns('',
		url(r'^problem/$', 'apps.author.views.authorProblemsView'),
		url(r'^problem/add$', 'apps.author.views.addProblem'),
		url(r'^problem/edit/(?P<problem_code>[A-Za-z0-9]+)/download/(?P<testcase_id>[A-Za-z0-9]+)/$', 'apps.author.views.downloadTestFile'),                   
		url(r'^problem/edit/(?P<problem_code>[A-Za-z0-9]+)/delete/(?P<testcase_id>[A-Za-z0-9]+)/$', 'apps.author.views.deleteTestFiles'),                   
		url(r'^problem/edit/(?P<problem_code>[A-Za-z0-9]+)/$', 'apps.author.views.editProblem'),		   
		)
