from apps.djangoratings.fields import RatingField
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from pygments.lexers import get_all_lexers


syntaxes = []

for lexer in get_all_lexers():
	lex = ( str(lexer[0]).lower(), lexer[0] )
	syntaxes.append( lex )

class Language( models.Model ):

	def __unicode__(self):
		return self.name
        CHOICE=[(1,'compiled'),(0,'intrepreted')]
		
	name = models.CharField( max_length=20 )
	extension = models.CharField( max_length=5 )
	compiler = models.CharField( max_length=10 )
	langType = models.BooleanField("Language type",choices=CHOICE)
	compileParam = models.CharField( "Compile Parameters", max_length=30, null = True, blank = True);
	syntax = models.CharField( max_length=20, choices= syntaxes )
	class Meta:
		db_table = 'language'

class TestCase( models.Model ):

	description = models.CharField( max_length=30 )
	input = models.FileField( 'Input', upload_to = 'dummy_field' )
	output = models.FileField( 'Output', upload_to = 'dummy_field')
	problem = models.ForeignKey( 'Problem' )
	class Meta:
		db_table = 'testcase'
        @classmethod
        def create(cls, ip,op,prob):
            testcaseobj = cls(input=ip,output=op,problem=prob)
            return testcaseobj

class Problem( models.Model ):
	
	def __unicode__(self):
		return self.code
	
	code = models.CharField( 'CODE', max_length=10, unique = True )
	title = models.CharField( 'Title', max_length=30 )
	description = models.TextField( 'Description')
	isVisible = models.BooleanField('Visible in Practice mode')
	solutionVisible = models.BooleanField('Solution Visible')
	dateAdded = models.DateField( 'Date Added', auto_now_add = True )
	author = models.ManyToManyField(  User )
	sourceLimit = models.IntegerField( 'Source Limit')
	timeLimit = models.IntegerField('Time Limit')
	memoryLimit = models.IntegerField('Memory Limit')
	languages = models.ManyToManyField( Language )
	difficulty = RatingField( range=5 )
	decimalJudgeOn=models.BooleanField('Decimal judge on (specify absolute error)')
	absoluteError=models.DecimalField('Allowed absolute error (switch on decimal judge)',max_digits=19, decimal_places=19)

	def success( self ):
		count = 0
		for submission in self.submission_set.all():
			if submission.status == 'ACC' and submission.contest is None:
				count += 1
		return count

	def solved( self, user, contest ):
		submissions = Submission.objects.filter( user = user, contest = contest )
		for submission in submissions:
			if submission.status == 'ACC':
				return True
		return False

	def practiceCount( self ):
		count = 0
		for submission in self.submission_set.all():
			if submission.contest is None:
				count += 1
		return count
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

