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
    url(r'^account/(?P<user_id>\d+)/$', 'online_judge.views.profile'),
    url(r'^account/(?P<user_id>\d+)/submissions$', submissionListView.as_view() ),
    url(r'^practice/', problemListView.as_view() ),

    url(r'^problem/(?P<pk>\d+)/$',  problemDetailView.as_view()),
    url(r'^problem/(?P<problem_id>\d+)/submit/$', 'judge.views.submit'),
    # url(r'^online_judge/', include('online_judge.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    url(r'^admin/', include(admin.site.urls)),
)
