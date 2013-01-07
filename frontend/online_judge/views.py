from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.contrib.auth import logout
from django.template import RequestContext
from django.contrib.auth.models import User
from judge.views import get_recent_activity
from judge.models import Submission

def home( request):
	if request.user.is_authenticated():
		submissions = Submission.objects.filter( user = request.user )[:10]
	else:
		submissions = None
	return render_to_response("index.html", {'recent_activity': get_recent_activity(), 'submissions': submissions }, context_instance=RequestContext(request) )



def logoutView( request ):
	logout( request )
	return redirect( home )

def profile( request, user_id ):
	user = get_object_or_404( User, pk=user_id )
	if user == request.user:
		if request.method == 'POST':
			user.first_name = request.POST['first_name']
			user.last_name = request.POST['last_name']
			user.email = request.POST['email']
			user.save()
			return redirect( home )
		return render_to_response( 'editable_profile.html', {'recent_activity': get_recent_activity() }, context_instance=RequestContext(request) )

	else:
		return render_to_response('basic_profile.html', { 'required_user': user, 'recent_activity': get_recent_activity() }, context_instance=RequestContext(request) )


