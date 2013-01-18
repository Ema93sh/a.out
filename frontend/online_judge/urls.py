from django.conf.urls import patterns, include, url
from judge.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'online_judge.views.home', name='home'),
    url(r'^account/logout$', 'online_judge.views.logoutView'),
    url(r'^account/login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^account/(?P<user_id>\d+)/$', 'online_judge.views.profile'),
    url(r'^account/(?P<user_id>\d+)/submissions$', submissionListView.as_view() ),
    url(r'^practice/', problemListView.as_view() ),
    url(r'^problem/(?P<pk>\d+)/$',  problemDetailView.as_view()),
    url(r'^problem/(?P<problem_id>\d+)/submit/$', 'judge.views.submit'),
    url(r'^submission/(?P<submission_id>\d+)/$', 'judge.views.submission'),
    url(r'^problem/(?P<problem_id>\d+)/comment/add$', 'judge.views.addComment'),
    
    url(r'^contest/$', contestListView.as_view() ),
    url(r'^contest/(?P<pk>\d+)/$', contestDetailView.as_view() ),
    url(r'^contest/(?P<contest_id>\d+)/problem/(?P<pk>\d+)/$', problemDetailView.as_view()),
    url(r'^contest/(?P<contest_id>\d+)/problem/(?P<problem_id>\d+)/submit$', 'judge.views.submit'),
    url(r'^contest/(?P<contest_id>\d+)/register', 'judge.views.register'),
    url(r'^contest/(?P<contest_id>\d+)/ranking', 'judge.views.ranking'),

    url(r'^author/problem$', 'judge.views.authorProblemsView'),
    url(r'^author/problem/add$', 'judge.views.addProblem'),
    url(r'^author/problem/edit/(?P<problem_id>\d+)/$', 'judge.views.editProblem'),

    
    url(r'^tinymce/', include('tinymce.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    url(r'^admin/', include(admin.site.urls)),
)
