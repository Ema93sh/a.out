from models import *
from forms import *
from apps.submission.models import *

from django.http import HttpResponseForbidden, HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.utils import timezone
from datetime import timedelta
from django.http import Http404

def get_recent_activity():
	return Submission.objects.order_by('-date')[:10]

class problemDetailView( DetailView ):
	model = Problem
	context_object_name = 'problem'
	slug_field = 'code'
	template_name = 'judge/problem.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(problemDetailView, self).get_context_data(**kwargs)
		context['recent_activity'] = get_recent_activity()
		return context


class problemListView( ListView ):
	model = Problem
	template_name = 'judge/practice.html'
	context_object_name = 'problems'
	queryset = Problem.objects.filter( isVisible = True )
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super( problemListView, self).get_context_data(**kwargs)
		context['recent_activity'] = get_recent_activity()
		return context


@login_required
def addComment( request, problem_code ):
	problem = get_object_or_404( Problem, code = problem_code)	
	comment = Comment( author=request.user, problem = problem,  data= request.POST['comment'] )
	comment.save()
	return redirect( request.POST['next'] )


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
def editProblem( request, problem_id ):
	problem = get_object_or_404( Problem, pk = problem_id )
	if request.method =='POST':
		form = ProblemForm( request.POST , request.FILES, instance = problem)
		if form.is_valid():
			form.save()
			return redirect('/author/problem')
	else:
		form = ProblemForm( instance = problem )
	return render_to_response('judge/author/edit_problem.html', {'form': form, 'problem' : problem}, context_instance = RequestContext( request ))


@login_required
def submit( request, problem_code ):
	problem = get_object_or_404( Problem, code=problem_code )
	if request.method == 'POST':
		form = SubmissionForm(request.POST, request.FILES)
		if form.is_valid():
			language = get_object_or_404( Language, pk= request.POST['language'] )
			submission = Submission( user=request.user, problem = problem, language = form.cleaned_data['language'], userCode = request.FILES['userCode'] );
			submission.save()
			jobqueue = JobQueue( submission = submission )
			jobqueue.save()
			return redirect( '/practice/problem/'+ problem_code )

	form = SubmissionForm(problem = problem)
	return render_to_response( 'judge/submit.html', { 'problem' : problem, 'form' : form, 'recent_activity': get_recent_activity() }, context_instance=RequestContext(request) )
