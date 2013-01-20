from models import *
from forms import *

from django.contrib import admin

class ProblemAdmin(admin.ModelAdmin):
	list_display = ('code', 'title', 'sourceLimit', 'timeLimit', 'memoryLimit', 'isVisible', 'solutionVisible', )
	list_filter = ( 'dateAdded', 'isVisible', 'languages')
	list_editable = ( 'isVisible', 'solutionVisible')
	filter_horizontal = ( 'author', 'languages' )
	fields = ( 'code', 'title', 'description',  'sourceLimit', 'timeLimit', 'memoryLimit', 'isVisible', 'inputFile', 'outputFile', 'author', 'languages', 'solutionVisible')
	form = ProblemForm

class CommentAdmin(admin.ModelAdmin):
	list_display = ('author', 'problem', 'data', 'date' )

admin.site.register( Language )
admin.site.register( Problem, ProblemAdmin )
admin.site.register( Comment, CommentAdmin )
