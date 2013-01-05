from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

# Create your models here.

class Language( models.Model ):

	def __unicode__(self):
		return self.name

	name = models.CharField( max_length=20 )
	extension = models.CharField( max_length=5 )
	compiler = models.CharField( max_length=10 )
	compileParam = models.CharField( "Compile Parameters", max_length=30 );
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
	isVisible = models.BooleanField('Visible' )
	dateAdded = models.DateField( 'Date Added', auto_now_add = True )
	author = models.ManyToManyField(  User )
	sourceLimit = models.IntegerField( 'Source Limit')
	timeLimit = models.IntegerField('Time Limit')
	memoryLimit = models.IntegerField('Memory Limit')
	languages = models.ManyToManyField( Language )

	class Meta:
		db_table = 'problems'

def submission_file_name(instance, filename):
	    return '/'.join(['submissions', instance.user.username, instance.problem.code, filename ])

class Submission( models.Model ):

	def __unicode__(self):
		return self.user.username
	STATUS_CODE  = (
			("ERR", "Internal Error"),
			("WAI", "Waiting"),
			("SUC", "Success"),
			("TLE", "Time Limit Exceeded"),
			("RTE", "Runtime Error"),
			("CTE", "Compile Time Error"),
			)
	date = models.DateTimeField( 'Date added', auto_now_add = True )
	user = models.ForeignKey( User )
	problem = models.ForeignKey( Problem )
	language = models.ForeignKey( Language )
	status = models.CharField( max_length=3, default="WAI", choices=STATUS_CODE)
	time = models.FloatField('Time Elapsed', null = True)
	memory = models.FloatField('Memory Used', null = True)
	userCode = models.FileField('User Program', upload_to = submission_file_name ) 
	class Meta:
		db_table = 'submissions'

class JobQueue( models.Model ):
	def __unicode__(self):
		return "test"

	submission = models.ForeignKey( Submission )

	class Meta:
		db_table = 'jobQueue'
