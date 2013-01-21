from models import *

from django.contrib import admin

class ContestAdmin( admin.ModelAdmin ):
        list_display = ( 'code', 'name', 'startTime', 'endTime', 'isActive' )
        filter_horizontal = ('problems',)
        fields = ( 'code', 'name', 'admin', 'startTime', 'endTime', 'problems',  'penalty_submission' ,)


admin.site.register( Contest, ContestAdmin )
