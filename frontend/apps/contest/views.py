from models import *
from forms import *
from apps.practice.models import *
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

class contestListView( ListView ):
        model = Contest
        template_name = 'judge/contest/contest.html'
        context_object_name = 'contests'
        queryset = Contest.objects.all()
        def get_context_data(self, **kwargs):
                # Call the base implementation first to get a context
                context = super( contestListView, self).get_context_data(**kwargs)
                context['recent_activity'] = get_recent_activity()
                context['past_contest'] = Contest.objects.filter( endTime__lt = timezone.now() )
                context['future_contest'] = Contest.objects.filter( startTime__gt = timezone.now() )
                return context

class contestDetailView( DetailView ):
        model = Contest
        template_name = 'judge/contest/contest_detail.html'
        context_object_name = 'contest'
	slug_field = 'code'

        def get_context_data(self, **kwargs):
                # Call the base implementation first to get a context
                context = super( contestDetailView, self).get_context_data(**kwargs)
                context['recent_activity'] = get_recent_activity()
                if self.request.user.is_authenticated():
                        solved_problems = [ 0, ]
                        no_of_submissions = { }
			succ_submissions = { }

			contest = self.get_object()
			for problem in contest.problems.all():
				submissions = Submission.objects.filter( contest = contest, problem = problem )
				no_of_submissions[problem.id] = 0
				succ_submissions[problem.id] = 0
				for submission in submissions:
					no_of_submissions[problem.id] += 1 
					if submission.status == 'ACC':
						succ_submissions[problem.id] += 1

			submissions = Submission.objects.filter( user = self.request.user , contest = self.get_object())
                        for submission in submissions:
                                if submission.status == 'ACC':
					if submission.problem.id not in solved_problems:
                                                solved_problems.append( submission.problem.id )
                      	print( no_of_submissions ) 
			context['succ_submissions'] = succ_submissions
			context['no_of_submissions'] = no_of_submissions
			context['solved_problem'] = solved_problems
                return context

class problemDetailView( DetailView ):
	model = Problem
	context_object_name = 'problem'
	slug_field = 'code'
	template_name = 'judge/contest/contest_problem.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(problemDetailView, self).get_context_data(**kwargs)
		context['recent_activity'] = get_recent_activity()
		context['contest'] = Contest.objects.get( code = self.kwargs['contest_code'] )
		return context




def calculateScore( user, contest ):
        score = 0
        penalty = 0
        total_time = timedelta(0)
        for problem in contest.problems.all():
                submissions = problem.submission_set.filter( user = user, contest = contest ).order_by('date')
                problem_submission_time = timedelta(0)
                for submission in submissions:
                        if submission.date < contest.endTime:
                                if submission.status == 'ACC':
                                        problem_submission_time = submission.date - contest.startTime
                                        score += 1
                                        break #till it encounters an accpeted solution, after the first accepted sol, all other submission for problem is ignored
                                elif (submission.status != 'WAI') and (submission.status != 'ERR'):
                                        penalty += (60 * 20 )
                if total_time < problem_submission_time:
                        total_time = problem_submission_time
	
	try:
		rank = Ranking.objects.get( contest = contest, user = user )
	except Ranking.DoesNotExist:
		rank = Ranking( contest = contest, user = user )
        total_time_seconds = total_time.total_seconds()
	rank.score = score
	rank.penalty = penalty
	rank.total_time_elapsed = total_time_seconds + penalty  #add 20 mins for each penalty
        rank.save()

        print("Score:" + str(rank.score))
        print("Penality:" + rank.formatedPenalty())
        print("total_time:" + str(rank.total_time_elapsed))

def calculateAllScores( contest ):
	for user in contest.users.all():
                calculateScore( user, contest )
	contest.ranking_update = timezone.now()
	contest.save()

def ranking( request, contest_code ):
        contest = get_object_or_404( Contest, code = contest_code )
	if contest.ranking_update:
		if contest.ranking_update < contest.endTime:
			calculateAllScores( contest )
	else:
		calculateAllScores( contest )

	ranks = Ranking.objects.filter( contest = contest ).order_by('-score', 'penalty', 'total_time_elapsed')
        return render_to_response('judge/contest/contest_ranking.html', { 'contest': contest, 'ranks': ranks }, context_instance=RequestContext(request) )


@login_required
def register( request, contest_code ):
        contest = get_object_or_404( Contest, code = contest_code )
        if contest.registration_end_time > timezone.now():
                if request.user not in contest.users.all():
                        contest.users.add( request.user )
                        rank = Ranking( contest = contest, user = request.user )
                        contest.save()
                        rank.save()
		else:
			return HttpResponse("User already registered")
        return redirect('/contest')

@login_required
def submit( request, problem_code, contest_code ):
        problem = get_object_or_404( Problem, code=problem_code )
        if request.method == 'POST':
                form = SubmissionForm(request.POST, request.FILES)
                if form.is_valid():
                        language = get_object_or_404( Language, pk= request.POST['language'] )
                        contest = get_object_or_404( Contest, code = contest_code )
                        if not contest.isActive:
				raise Http404
			if request.user not in contest.users.all():
                                raise Http404 #Should modify to tell that user is not registered
                        submission = Submission( user=request.user, problem = problem, contest = contest, language = form.cleaned_data['language'], userCode = request.FILES['userCode'] );
                        submission.save()
                        jobqueue = JobQueue( submission = submission )
                        jobqueue.save()
                        return redirect( '/contest/' + contest_code + '/problem/' + problem_code )

        form = SubmissionForm(problem = problem)
	contest = get_object_or_404( Contest, code = contest_code )
	if contest.isActive():
		if request.user not in contest.users.all():
			raise Http404
                if not contest.isActive():
                        return redirect( '/contest/' + contest_code )
	return render_to_response( 'judge/contest/submit.html', {  'contest': contest, 'problem' : problem, 'form' : form, 'recent_activity': get_recent_activity() }, context_instance=RequestContext(request) )
