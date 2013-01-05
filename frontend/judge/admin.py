from judge.models import Problem, Language, Submission, JobQueue
from django.contrib import admin


class ProblemAdmin(admin.ModelAdmin):
	list_display = ('code', 'title', 'sourceLimit', 'timeLimit', 'memoryLimit', 'isVisible')
	list_filter = ( 'dateAdded', 'isVisible', 'languages')
	list_editable = ( 'isVisible', )
	filter_horizontal = ( 'author', 'languages' )
	fields = ( 'code', 'title', 'description',  'sourceLimit', 'timeLimit', 'memoryLimit', 'isVisible', 'inputFile', 'outputFile', 'author', 'languages', )

class SubmissionAdmin( admin.ModelAdmin ):
	list_display = ( 'user', 'problem', 'status', 'language', 'time', 'memory', )
	list_filter = ( 'date', 'status', 'language')
	fields = ( 'user', 'problem', 'language', 'userCode', )
admin.site.register( Language )
admin.site.register( Problem, ProblemAdmin )
admin.site.register( Submission, SubmissionAdmin )
admin.site.register( JobQueue )
