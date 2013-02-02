from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.contrib.auth import logout
from django.template import RequestContext
from django.contrib.auth.models import User
from forms import *

def registerUser(request):
   msg=''
   if request.method == 'POST':
      form = registrationForm( request.POST)
      if request.POST['password']==request.POST['confirmPassword']:
         user=User.objects.create_user(request.POST['username'],'',request.POST['password'])
         user.save()
         return redirect( '/')
      else:
         msg='registration not successfull either passwords dont match or username already exists'
         return render_to_response('register.html', { 'form':form,'msg':msg}, context_instance=RequestContext(request) )
   else:
      form = registrationForm()
      return render_to_response('register.html', { 'form':form,'msg':msg}, context_instance=RequestContext(request) )
   