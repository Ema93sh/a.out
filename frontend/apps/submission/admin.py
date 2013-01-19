from models import *

from django.contrib import admin


class SubmissionAdmin( admin.ModelAdmin ):
        list_display = ( 'user', 'problem', 'status', 'language', 'time', 'memory','contest' )
        list_filter = ( 'date', 'status', 'language', 'contest')
        fields = ( 'user', 'problem', 'language', 'userCode', 'contest',)


admin.site.register( Submission, SubmissionAdmin )
admin.site.register( JobQueue )
