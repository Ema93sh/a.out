from views import *

from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()

urlpatterns = patterns('',
                   url(r'^$', submissionListView.as_view() ),
		   url(r'view/(?P<submission_id>\d+)/$', 'apps.submission.views.viewSubmission'),
		   url(r'^download/(?P<submission_id>\d+)/$', 'apps.submission.views.downloadSubmission'),
		   
		   url(r'^problem/(?P<problem_code>[A-Za-z0-9]+)/$', submissionListView.as_view() ),

		   url(r'^contest/(?P<contest_code>\w+)/problem/(?P<problem_code>\w+)', submissionListView.as_view() ),
		   url(r'^contest/(?P<contest_code>\w+)/(?P<user_name>\w+)/(?P<problem_code>[A-Za-z0-9]+)/$', submissionListView.as_view() ),
		   url(r'^contest/(?P<contest_code>\w+)/(?P<user_name>\w+)/$', submissionListView.as_view() ),
		   url(r'^contest/(?P<contest_code>\w+)/', submissionListView.as_view() ),


		   url(r'^(?P<user_name>\w+)/(?P<problem_code>[A-Za-z0-9]+)/$', submissionListView.as_view() ),
		   url(r'^(?P<user_name>\w+)/$', submissionListView.as_view() ),
		   )
