from judge.models import Contest, Problem, Language, Submission, JobQueue, Comment
from django.contrib import admin
from judge.forms import *

class ProblemAdmin(admin.ModelAdmin):
	list_display = ('code', 'title', 'sourceLimit', 'timeLimit', 'memoryLimit', 'isVisible', 'solutionVisible', )
	list_filter = ( 'dateAdded', 'isVisible', 'languages')
	list_editable = ( 'isVisible', )
	filter_horizontal = ( 'author', 'languages' )
	fields = ( 'code', 'title', 'description',  'sourceLimit', 'timeLimit', 'memoryLimit', 'isVisible', 'inputFile', 'outputFile', 'author', 'languages', )
	form = ProblemForm

class SubmissionAdmin( admin.ModelAdmin ):
	list_display = ( 'user', 'problem', 'status', 'language', 'time', 'memory','contest' )
	list_filter = ( 'date', 'status', 'language', 'contest')
	fields = ( 'user', 'problem', 'language', 'userCode', 'contest',)

class ContestAdmin( admin.ModelAdmin ):
	list_display = ( 'code', 'name', 'startTime', 'endTime', 'isActive' )
	filter_horizontal = ('problems', 'users')
	fields = ( 'code', 'name', 'admin', 'startTime', 'endTime', 'problems',  'penalty_submission' , 'users')

admin.site.register( Language )
admin.site.register( Problem, ProblemAdmin )
admin.site.register( Submission, SubmissionAdmin )
admin.site.register( JobQueue )
admin.site.register( Contest, ContestAdmin )
admin.site.register( Comment )
