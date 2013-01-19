from forms import *
from apps.practice.models import *

from django.http import HttpResponseForbidden, HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.utils import timezone
from datetime import timedelta
from django.http import Http404

@login_required
def authorProblemsView( request ):
        if request.user.groups.filter( name='Authors'):
                return render_to_response( 'judge/author/problems.html', { }, context_instance = RequestContext( request ) )
        raise Http404

@login_required
def addProblem( request ):
        if request.method =='POST':
                form = ProblemForm( request.POST , request.FILES)
                if form.is_valid():
                        form.save()
                        return redirect('/author/problems')
        else:
                form = ProblemForm()

        return render_to_response('judge/author/add_problem.html', {'form': form}, context_instance = RequestContext( request ))


@login_required
def editProblem( request, problem_code ):
        problem = get_object_or_404( Problem, code = problem_code )
        if request.method =='POST':
                form = ProblemForm( request.POST , request.FILES, instance = problem)
                if form.is_valid():
                        form.save()
                        return redirect('/author/problem/')
        else:
                form = ProblemForm( instance = problem )
        return render_to_response('judge/author/edit_problem.html', {'form': form, 'problem' : problem}, context_instance = RequestContext( request ))
