from models import *
from apps.practice.models import *
from apps.contest.models import *

from django.http import HttpResponseForbidden, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.utils import timezone
from datetime import timedelta
from django.http import Http404

def get_recent_activity():
        return Submission.objects.order_by('-date')[:10]

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
		queryset = Submission.objects.all()
		if 'username' in self.kwargs:
			user = get_object_or_404( User, username = self.kwargs['username'] )
			queryset = queryset.filter( user = user )
		if 'contest_code' in self.kwargs:
			contest = get_object_or_404( Contest, code = self.kwargs['contest_code'] )
			queryset = queryset.filter( contest = contest )
		if 'problem_code' in self.kwargs:
			problem = get_object_or_404( Problem, code = self.kwargs['problem_code'] )
			queryset = queryset.filter( problem = problem )
		return queryset.order_by('-date')




def submission( request, submission_id ):
        submission = get_object_or_404( Submission, pk=submission_id )
        if not submission.problem.solutionVisible:
                return HttpResponseForbidden("You do not have permission to view this link")
        filename = submission.user.username + "_" + submission.problem.code +"_" + str(submission.id)
        response = HttpResponse( submission.userCode, content_type="text/plain" )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


