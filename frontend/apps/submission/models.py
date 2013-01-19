from apps.contest.models import *
from apps.practice.models import *
from django.contrib.auth.models import User

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

