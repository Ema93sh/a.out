from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.contrib.auth import logout
from django.template import RequestContext

def home( request):
	return render_to_response("index.html", { }, context_instance=RequestContext(request) )

def logoutView( request ):
	logout( request )
	return redirect( home )
