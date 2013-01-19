from tinymce.models import HTMLField
from apps.djangoratings.fields import RatingField
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

CHOICE=[(1,'compiled'),(0,'intrepreted')]
class Language( models.Model ):

	def __unicode__(self):
		return self.name

	name = models.CharField( max_length=20 )
	extension = models.CharField( max_length=5 )
	compiler = models.CharField( max_length=10 )
	langType = models.BooleanField("Language type",choices=CHOICE)
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
	description = models.TextField( 'Description')
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

	def __unicode__(self):
		return self.data

	author = models.ForeignKey(  User )
	date = models.DateTimeField('Date Added', auto_now_add = True)
	data = models.TextField('Comment')
	#replies = models.ManyToManyField( Comment )
	approved = models.BooleanField('is Approved', default = True)
	problem = models.ForeignKey( Problem )

