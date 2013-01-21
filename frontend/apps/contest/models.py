from apps.practice.models import *
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

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
	ranking_update = models.DateTimeField( null = True)

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

	def problemSolved( self ):
		return self.score

	def formatedPenalty( self):
		p = timedelta(0,self.penalty)
		return str(p)

	def totalTime( self ):
		p = timedelta(0,self.total_time_elapsed)
		return str(p)

        class Meta:
                db_table = 'score'
                ordering = ['-score', 'penalty', '-total_time_elapsed']

