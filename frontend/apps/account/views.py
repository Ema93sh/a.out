from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.contrib.auth import logout
from django.template import RequestContext
from django.contrib.auth.models import User
from forms import *
from apps.submission.models import *
from collections import OrderedDict
from apps.practice.views import get_recent_activity
from django.conf import settings


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
      
def registerUser(request):
   msg=''
   if request.method == 'POST':
      form = registrationForm( request.POST)
      if form.is_valid() and request.POST['password']==request.POST['confirmPassword']:
         user=User.objects.create_user(request.POST['username'],'',request.POST['password'])
         user.save()
         return redirect( '/')
      else:
         msg='registration not successfull because wrong captcha ,passwords dont match or username already exists'
         return render_to_response('register.html', { 'form':form,'msg':msg}, context_instance=RequestContext(request) )
   else:
      form = registrationForm()
      return render_to_response('register.html', { 'form':form,'msg':msg}, context_instance=RequestContext(request) )
   
