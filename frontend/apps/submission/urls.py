from views import *

from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()

urlpatterns = patterns('',
                   url(r'^$', submissionListView.as_view() ),
                   url(r'^(?P<submission_id>\d+)/$', 'apps.submission.views.submission'),
                   )
