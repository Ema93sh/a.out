from django.http import HttpResponse
from judge.models import Problem, Language, Submission, JobQueue
from judge.forms import *
from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView

def get_recent_activity():
	return Submission.objects.order_by('-date')[:10]

class problemDetailView( DetailView ):
	model = Problem
	template_name = 'judge/problem.html'
	context_object_name = 'problem'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(problemDetailView, self).get_context_data(**kwargs)
		context['recent_activity'] = get_recent_activity()
		return context

class submissionListView( ListView ):
	model = Submission
	template_name = 'judge/submissions.html'
	context_object_name = 'submissions'
	paginate_by = 10
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super( submissionListView, self).get_context_data(**kwargs)
		context['recent_activity'] = get_recent_activity()
		return context

	def get_queryset( self ):
		return Submission.objects.filter( user = self.request.user ).order_by('-date')

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
def submit( request, problem_id ):
	problem = get_object_or_404( Problem, pk=problem_id )
	if request.method == 'POST':
		form = SubmissionForm(request.POST, request.FILES)
		if form.is_valid():
			language = get_object_or_404( Language, pk= request.POST['language'] )
			submission = Submission( user=request.user, problem = problem, language = form.cleaned_data['language'], userCode = request.FILES['userCode'] );
			submission.save()
			jobqueue = JobQueue( submission = submission )
			jobqueue.save()
			return redirect( '/problem/'+ problem_id )

	form = SubmissionForm(problem = problem)
	return render_to_response( 'judge/submit.html', { 'problem' : problem, 'form' : form, 'recent_activity': get_recent_activity() }, context_instance=RequestContext(request) )
