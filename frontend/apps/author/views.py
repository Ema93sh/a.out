from forms import *
from apps.practice.models import *
from apps.database_files.models import *

from django.http import HttpResponseForbidden, HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.utils import timezone
from datetime import timedelta
from django.http import Http404
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory

from StringIO import StringIO  
from zipfile import ZipFile  

def upload_files_toDB(Files,problem):
   n=len(Files)//2
   for f in range(n):
      testcase=TestCase.create(Files['form-'+str(f)+'-inputFile'],Files['form-'+str(f)+'-outputFile'],problem)
      testcase.save()
@login_required
def authorProblemsView( request ):
        if request.user.groups.filter( name='Authors'):
                return render_to_response( 'judge/author/problems.html', { }, context_instance = RequestContext( request ) )
        raise Http404

@login_required
def addProblem( request ):
        tformset=formset_factory(TestCaseForm,extra=2)
        if request.method =='POST':
                form = ProblemForm( request.POST , request.FILES)
                #tformset=TestCaseFormSet(request.POST,request.FILES)
                if form.is_valid() :
                        form.save()
                        problem=get_object_or_404( Problem, code = request.POST['code'])
                        #save each forms file with an id in data_files_file and add that id to testcase table'''
                        print request.FILES
                        upload_files_toDB(request.FILES,problem)
                        return redirect('/author/problem/')
        else:
                form = ProblemForm()
                tformset = formset_factory(TestCaseForm,extra=2)

        return render_to_response('judge/author/add_problem.html', {'form': form,'tformset':tformset}, context_instance = RequestContext( request ))


@login_required
def editProblem( request, problem_code ):
        problem = get_object_or_404( Problem, code = problem_code )
        testcase= TestCase.objects.filter(problem=problem)
        curr=len(testcase)
        tcdic=[]
        for tc in testcase:
           tcdic.append(tc.pk)
        if request.method =='POST':
                form = ProblemForm( request.POST , request.FILES, instance = problem)
                if form.is_valid():
                        form.save()
                        upload_files_toDB(request.FILES,problem)
                        return redirect('/author/problem/')
        else:
                form = ProblemForm( instance = problem )
                tformset=formset_factory(TestCaseForm)
        return render_to_response('judge/author/edit_problem.html', {'form': form, 'problem' : problem,'tformset':tformset,'testcase':tcdic}, context_instance = RequestContext( request ))
@login_required
def deleteTestFiles(request,problem_code,testcase_id):
   #check if the guy is allowed to do this
   tc=get_object_or_404(TestCase,pk=testcase_id)
   tc.input.delete()
   tc.output.delete()
   tc.delete()
   return redirect('/author/problem/edit/'+problem_code);
   
@login_required
def downloadTestFile(request,problem_code,testcase_id):
   #check if user is allowed to do this
   tc=get_object_or_404(TestCase,pk=testcase_id)
   in_memory = StringIO()
   zip = ZipFile(in_memory, "a")
   
   zip.writestr("inputfile.txt", tc.input.read())
   zip.writestr("outputfile.txt",tc.output.read() )
   
   # fix for Linux zip files read in Windows
   for file in zip.filelist:
      file.create_system = 0    
      
      zip.close()
      
      response = HttpResponse(mimetype="application/zip")
      response["Content-Disposition"] = "attachment; filename=tescasefile.zip"
      
      in_memory.seek(0)    
      response.write(in_memory.read())
      
      return response
      
      