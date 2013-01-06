from django.http import HttpResponse
from judge.models import Problem, Language, Submission, JobQueue
from judge.forms import *
from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required

def practice( request ):
	problems = Problem.objects.filter( isVisible = True ).order_by('dateAdded')
	return render_to_response( 'judge/practice.html', {'problems' : problems },  context_instance=RequestContext(request) )


def problem( request, problem_id):
	problem = get_object_or_404( Problem, pk=problem_id )
	return render_to_response( 'judge/problem.html', { 'problem' : problem }, context_instance=RequestContext(request) )

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
	return render_to_response( 'judge/submit.html', { 'problem' : problem, 'form' : form }, context_instance=RequestContext(request) )
