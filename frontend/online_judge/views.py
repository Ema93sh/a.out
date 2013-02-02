
from apps.practice.views import get_recent_activity
from apps.practice.models import *
from apps.submission.models import *

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.contrib.auth import logout
from django.template import RequestContext
from django.contrib.auth.models import User



def home( request):
	if request.user.is_authenticated():
		submissions = Submission.objects.filter( user = request.user )[:10]
	else:
		submissions = None
	return render_to_response("index.html", {'recent_activity': get_recent_activity(), 'submissions': submissions }, context_instance=RequestContext(request) )

def logoutView( request ):
	logout( request )
	return redirect( home )
  