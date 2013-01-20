from views import *

from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()

urlpatterns = patterns('',
		    url(r'^$', contestListView.as_view() ),
		    url(r'^(?P<slug>[A-Za-z0-9]+)/$', contestDetailView.as_view() ),
		    url(r'^(?P<contest_code>[A-Za-z0-9]+)/problem/(?P<slug>[A-Za-z0-9]+)/$', problemDetailView.as_view()),
		    url(r'^(?P<contest_code>[A-Za-z0-9]+)/problem/(?P<problem_code>[A-Za-z0-9]+)/submit$', 'apps.contest.views.submit'),
		    url(r'^(?P<contest_code>[A-Za-z0-9]+)/register', 'apps.contest.views.register'),
		    url(r'^(?P<contest_code>[A-Za-z0-9]+)/ranking', 'apps.contest.views.ranking'),
		   )
