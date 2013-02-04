from models import *
from apps.practice.models import *
from apps.contest.models import *
from apps.database_files.models import *

import os
from django.http import HttpResponseForbidden, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.utils import timezone
from datetime import timedelta
from django.http import Http404
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


styles = list(get_all_styles())
syntaxes = [lexer[0] for lexer in get_all_lexers()]

def get_recent_activity():
        return Submission.objects.order_by('-date')[:10]

class submissionListView( ListView ):
        model = Submission
        template_name = 'judge/submission/submissions.html'
        context_object_name = 'submissions'

	def get_context_data(self, **kwargs):
                # Call the base implementation first to get a context
                context = super( submissionListView, self).get_context_data(**kwargs)
                context['recent_activity'] = get_recent_activity()
		if 'user_name' in self.kwargs:
			context['user_name'] = self.kwargs['user_name']
		if 'contest_code' in self.kwargs:
			context['contest_code'] = self.kwargs['contest_code']
		if 'problem_code' in self.kwargs:
	       		context['problem_code'] = self.kwargs['problem_code']
		return context

        def get_queryset( self ):
		queryset = Submission.objects.all().order_by("-date")
		if 'user_name' in self.kwargs:
			user = get_object_or_404( User, username = self.kwargs['user_name'] )
			queryset = queryset.filter( user = user )
		if 'contest_code' in self.kwargs:
			contest = get_object_or_404( Contest, code = self.kwargs['contest_code'] )
			queryset = queryset.filter( contest = contest )
		if 'problem_code' in self.kwargs:
			problem = get_object_or_404( Problem, code = self.kwargs['problem_code'] )
			queryset = queryset.filter( problem = problem )
		return queryset.order_by('-date')


def viewSubmission( request, submission_id ):
	submission = get_object_or_404( Submission, pk=submission_id )
	if submission.contest:
           if submission.contest.isActive() and submission.user != request.user:
              return HttpResponseForbidden("You do not have permission to view this link")
        
        if not submission.problem.solutionVisible and submission.user != request.user:
           return HttpResponseForbidden("You do not have permission to view this link")
	
	code = submission.userCode.read()
	syntax = str(submission.language.syntax).lower()
	return render_to_response( 'judge/submission/view_solution.html',  { 'code': code, 'submission': submission, 'syntax': syntax, 'style': 'manni', 'recent_activity': get_recent_activity() }, context_instance=RequestContext(request))

@login_required
def downloadSubmission( request, submission_id ):
        submission = get_object_or_404( Submission, pk=submission_id )
        if submission.contest:
           if submission.contest.isActive() and submission.user != request.user:
              return HttpResponseForbidden("You do not have permission to view this link")
        if not submission.problem.solutionVisible and submission.user != request.user:
                return HttpResponseForbidden("You do not have permission to view this link")
        filename = submission.user.username + "_" + submission.problem.code +"_" + str(submission.id)
	code = submission.userCode.read()
	response = HttpResponse( code , content_type="text/plain" )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename+str(submission.language.extension)
        return response


