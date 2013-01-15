from django.http import HttpResponseForbidden, HttpResponse
from judge.models import Contest, Problem, Language, Submission, JobQueue
from judge.forms import *
from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.http import Http404

def get_recent_activity():
	return Submission.objects.order_by('-date')[:10]

class problemDetailView( DetailView ):
	model = Problem
	context_object_name = 'problem'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(problemDetailView, self).get_context_data(**kwargs)
		context['recent_activity'] = get_recent_activity()
		if 'contest_id' in self.kwargs:
			context['contest'] = Contest.objects.get( id = self.kwargs['contest_id'] )
		return context

	def get_template_names(self):
		if 'contest_id' in self.kwargs:
			return ['judge/contest_problem.html',]
		else:
			return ['judge/problem.html',]

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

class contestListView( ListView ):
	model = Contest
	template_name = 'judge/contest.html'
	context_object_name = 'contests'
	queryset = Contest.objects.filter( startTime__lt = timezone.now(), endTime__gt = timezone.now() )
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super( contestListView, self).get_context_data(**kwargs)
		context['recent_activity'] = get_recent_activity()
		context['past_contest'] = Contest.objects.filter( endTime__lt = timezone.now() )
		context['future_contest'] = Contest.objects.filter( startTime__gt = timezone.now() )
		return context

class contestDetailView( DetailView ):
	model = Contest
	template = 'judge/contest_detail.html'
	context_object_name = 'contest'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super( contestDetailView, self).get_context_data(**kwargs)
		context['recent_activity'] = get_recent_activity()
		return context


@login_required
def addComment( request, problem_id ):
	problem = get_object_or_404( Problem, pk = problem_id)	
	comment = Comment( author=request.user, problem = problem,  data= request.POST['comment'] )
	comment.save()
	return redirect( request.POST['next'] )


@login_required
def authorProblemsView( request ):
	if request.user.groups.filter( name='Authors'):
		return render_to_response( 'judge/author/problems.html', { }, context_instance = RequestContext( request ) )
	raise Http404

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
			return redirect('author/problems')
	else:
		form = ProblemForm( instance = problem )
	return render_to_response('judge/author/edit_problem.html', {'form': form, 'problem' : problem}, context_instance = RequestContext( request ))

def submission( request, submission_id ):
	submission = get_object_or_404( Submission, pk=submission_id )
	if not submission.problem.solutionVisible:
		return HttpResponseForbidden("You do not have permission to view this link")
	filename = submission.user.username + "_" + submission.problem.code +"_" + str(submission.id)
	response = HttpResponse( submission.userCode, content_type="text/plain" )
	response['Content-Disposition'] = 'attachment; filename=%s' % filename
	return response


@login_required
def submit( request, problem_id, contest_id = None ):
	problem = get_object_or_404( Problem, pk=problem_id )
	if request.method == 'POST':
		form = SubmissionForm(request.POST, request.FILES)
		if form.is_valid():
			language = get_object_or_404( Language, pk= request.POST['language'] )
			contest = None
			if contest_id:
				contest = get_object_or_404( Contest, pk = contest_id )
				if not contest.isActive:
					raise Http404
			submission = Submission( user=request.user, problem = problem, contest = contest, language = form.cleaned_data['language'], userCode = request.FILES['userCode'] );
			submission.save()
			jobqueue = JobQueue( submission = submission )
			jobqueue.save()
			if contest_id:
				return redirect( '/contest/' + contest_id + '/problem/' + problem_id )
			return redirect( '/problem/'+ problem_id )

	form = SubmissionForm(problem = problem)
	inContest = False
	if contest_id:
		inContest = True
		contest = get_object_or_404( Contest, pk = contest_id )
		if not contest.isActive():
			return redirect( '/contest/' + contest_id )
	return render_to_response( 'judge/submit.html', { 'inContest': inContest, 'problem' : problem, 'form' : form, 'recent_activity': get_recent_activity() }, context_instance=RequestContext(request) )
