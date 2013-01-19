from views import *
from apps.practice.views import *

from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()

urlpatterns = patterns('',
		    url(r'^$', contestListView.as_view() ),
		    url(r'^(?P<slug>\d+)/$', contestDetailView.as_view() ),
		    url(r'^(?P<contest_code>[A-Za-z]+)/problem/(?P<slug>[A-Za-z]+)/$', problemDetailView.as_view()),
		    url(r'^(?P<contest_code>[A-Za-z]+)/problem/(?P<problem_id>\d+)/submit$', 'apps.contest.views.submit'),
		    url(r'^(?P<contest_code>[A-Za-z]+)/register', 'apps.contest.views.register'),
		    url(r'^(?P<contest_code>[A-Za-z]+)/ranking', 'apps.contest.views.ranking'),
		   )
