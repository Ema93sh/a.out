from collections import OrderedDict

from apps.practice.views import get_recent_activity
from apps.practice.models import *
from apps.submission.models import *

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.contrib.auth import logout
from django.template import RequestContext
from django.contrib.auth.models import User

def solvedProblems(user):
   acuser=Submission.objects.filter(user=user,status = 'ACC')
   solved=OrderedDict()
   solved['practice']=[]
   for s in acuser:
      if s.contest:
         solved[str(s.contest.code)]=[]
         
   for s in acuser:
      pcode=str(s.problem.code)
      ccode=str(s.contest.code) if s.contest else 'practice' 
      if pcode not in solved[ccode]: solved[ccode].append(pcode)
   return solved

def home( request):
	if request.user.is_authenticated():
		submissions = Submission.objects.filter( user = request.user )[:10]
	else:
		submissions = None
	return render_to_response("index.html", {'recent_activity': get_recent_activity(), 'submissions': submissions }, context_instance=RequestContext(request) )

def logoutView( request ):
	logout( request )
	return redirect( home )

def profile( request, user_name ):
	user = get_object_or_404( User, username=user_name )
	solved=solvedProblems(user)
	return render_to_response('basic_profile.html', { 'required_user': user, 'solved_problems':solved ,'recent_activity': get_recent_activity() }, context_instance=RequestContext(request) )
	
def editprofile(request, user_name):
   user = get_object_or_404( User, username=user_name )
   if user == request.user:
      if request.method == 'POST':
         user.first_name = request.POST['first_name']
         user.last_name = request.POST['last_name']
         user.email = request.POST['email']
         user.save()
         return redirect( '/account/'+user.username )
      return render_to_response('editable_profile.html', {'recent_activity': get_recent_activity() }, context_instance=RequestContext(request) )
         
   else:
      return redirect( '/account/'+user.username )     