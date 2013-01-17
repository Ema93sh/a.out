from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from djangoratings.fields import RatingField
from django.utils import timezone
# Create your models here.


class Language( models.Model ):

	def __unicode__(self):
		return self.name

	name = models.CharField( max_length=20 )
	extension = models.CharField( max_length=5 )
	compiler = models.CharField( max_length=10 )
	compileParam = models.CharField( "Compile Parameters", max_length=30, null = True, blank = True);
	class Meta:
		db_table = 'language'

def problem_input_file_name( instance, filename):
	return '/'.join(['problems', instance.code, 'input'])

def problem_output_file_name( instance, filename):
	return '/'.join(['problems', instance.code, 'output'])

class Problem( models.Model ):
	
	def __unicode__(self):
		return self.code
	
	code = models.CharField( 'CODE', max_length=10, unique = True )
	title = models.CharField( 'Title', max_length=30 )
	description = models.TextField( 'Description' )
	inputFile = models.FileField( 'Sample Input', upload_to = problem_input_file_name)
	outputFile = models.FileField( 'Sample Output', upload_to = problem_output_file_name)
	isVisible = models.BooleanField('Visible in Practice mode')
	solutionVisible = models.BooleanField('Solution Visible')
	dateAdded = models.DateField( 'Date Added', auto_now_add = True )
	author = models.ManyToManyField(  User )
	sourceLimit = models.IntegerField( 'Source Limit')
	timeLimit = models.IntegerField('Time Limit')
	memoryLimit = models.IntegerField('Memory Limit')
	languages = models.ManyToManyField( Language )
	difficulty = RatingField( range=5 )

	def success( self ):
		count = 0
		for submission in self.submission_set.all():
			if submission.status == 'ACC':
				count += 1
		return count

	def solved( self, user, contest ):
		submissions = Submission.objects.filter( user = user, contest = contest )
		for submission in submissions:
			if submission.status == 'ACC':
				return True
		return False

	class Meta:
		db_table = 'problems'

class Comment( models.Model ):
	author = models.ForeignKey( User )
	date = models.DateTimeField(auto_now_add = True)
	data = models.TextField()
	#replies = models.ManyToManyField( Comment )
	approved = models.BooleanField(default = True)
	problem = models.ForeignKey( Problem )

class Contest( models.Model ):
	def __unicode__(self):
		return self.name

	code = models.CharField( 'Code', max_length=7, unique=True )
	name = models.CharField( 'Name', max_length=30 )
	problems = models.ManyToManyField( Problem )
	startTime = models.DateTimeField()
	endTime = models.DateTimeField()
	admin = models.ForeignKey( User, related_name = "admin+") 
	users = models.ManyToManyField( User , blank = True)
	penalty_submission = models.BooleanField( 'Penalty for Wrong submission' )
	
	def isActive( self ):
		if self.startTime <= timezone.now() <= self.endTime:
			return True
		else:
			return False
	isActive.boolean = True
	isActive.short_description = 'Is contest Active?'

	class Meta:
		db_table = 'contest'
		ordering = ['-startTime']

class Ranking( models.Model ):
	contest = models.ForeignKey( Contest )
	user = models.ForeignKey( User )
	score = models.IntegerField( default = 0 )
	penalty = models.IntegerField( default = 0 )
	total_time_elapsed = models.IntegerField( default = 0 )
	
	class Meta:
		db_table = 'score'
		ordering = ['-score', 'penalty', '-total_time_elapsed']

def submission_file_name(instance, filename):
	    return '/'.join(['submissions', instance.user.username, instance.problem.code, filename ])

class Submission( models.Model ):

	def __unicode__(self):
		return self.user.username
	STATUS_CODE  = (
			("ERR", "Internal Error"),
			("WAI", "Waiting"),
			("ACC", "Accpeted"),
			("TLE", "Time Limit Exceeded"),
			("RTE", "Runtime Error"),
			("CTE", "Compile Time Error"),
			("WRA", "Wrong Answer"),
			)
	date = models.DateTimeField( 'Date added', auto_now_add = True )
	user = models.ForeignKey( User )
	problem = models.ForeignKey( Problem )
	language = models.ForeignKey( Language )
	status = models.CharField( max_length=3, default="WAI", choices=STATUS_CODE)
	time = models.FloatField('Time Elapsed', null = True)
	memory = models.FloatField('Memory Used', null = True)
	userCode = models.FileField('User Program', upload_to = submission_file_name ) 
	contest = models.ForeignKey( Contest , null = True)
	class Meta:
		db_table = 'submissions'

class JobQueue( models.Model ):
	def __unicode__(self):
		return "test"

	submission = models.ForeignKey( Submission )

	class Meta:
		db_table = 'jobQueue'
