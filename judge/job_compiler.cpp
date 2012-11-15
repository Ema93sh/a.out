//g++ job_compiler.cpp `mysql_config --cflags --libs`

#include <iostream>
#include <string>
#include <map>
#include "database.h"

using namespace std;


/* Input: JobID
 *   Output: Result of compilation( CME, WA, TLE, RE, etc )
 *   for now assuming jobid is the filename of source program
 */

class JobCompiler
{
private:
   double timeElapsed;
   string workingDir;
   string str,lang;
   string jobId;
   bool error; 
   string timeLimit,sourceLimit,memoryLimit;
   string problemCode;
   int result; // 0 - success, 1 - CME , 2 - RE, 3 - TLE, 4 - WA ,5 - AC
   string strResult; // converted result code to string
   map<string,int> srcType; // maps sourceType
   map<int,string> compileParam;//maps sourceType to compile parameters
   map<int,string> runParam;
   map<int,string> ext;
   int sourceType; // 1 - c , 2 - c++, 3 - python
   Database *db;

public:
   string stringBuilder(string path){
      FILE *inp=fopen(path.c_str(),"r");
      string ret="";
      char c;
      while((c=fgetc(inp))!=EOF){
         if(!(c==' '||c=='\t'||c=='\n'))
         ret+=c;
      }
      fclose(inp);
      return ret;
   }
   JobCompiler( string jid )
   {
      workingDir="/tmp/online_judge/";
      srcType["C"]=1;
      srcType["CPP"]=2;
      srcType["Python"]=3;
      
      error = false;
      jobId = jid;
      result = 0;
      timeElapsed=0.0;
      
      ext[1]=".c";
      ext[2]=".cpp";
      ext[3]=".py";
      compileParam[1]="gcc -o "+workingDir+"output "+workingDir+jobId+".c";
      compileParam[2]="g++ -o "+workingDir+"output "+workingDir+jobId+".cpp";
      runParam[1]=workingDir+"./output";
      runParam[2]=workingDir+"./output";
      runParam[3]="python "+workingDir+jobId+".py";
      

      db = new Database();
      db->initialize();
      db->connect();
   }
   
   void doWork()
   {
      checkType();
      compileIt();
      runIt();
      checkOutput();
   }
   
   void checkType()
   {
      MYSQL_ROW row;
      str="SELECT * FROM submissions WHERE submissionId=\""+jobId+"\" LIMIT 1";
      db->setQuery(str);
      db->useQuery();
      row= db->getRow();
      lang.assign(row[2]);
      problemCode.assign(row[1]);
      sourceType=srcType[lang];
      db->freeResult();
      //if it is an interpreted language call runIt
      //else call compileIt
   }
   
   void compileIt()
   {
      system(("cp ../data/users/testuser/"+jobId+ext[sourceType]+" "+workingDir+jobId+ext[sourceType]).c_str());
      if(!(sourceType==1||sourceType==2))return; // if not compiled languages
      //copy file to workingDir and work there
      //insert actual username here
      result = system(compileParam[sourceType].c_str());
      if( result != 0 )
      {
         error = true;
         result = 1;
      }
   }   
   void runIt()
   {
      if(error)return;
      int ret;
      MYSQL_ROW row;
      struct timeval begin, end; //for calculating time elapsed
      str="SELECT * FROM problems WHERE problemCode=\""+problemCode+"\" LIMIT 1";
      db->setQuery(str);
      db->useQuery();
      row=db->getRow();
      timeLimit.assign(row[5]);
      sourceLimit.assign(row[4]);
      memoryLimit.assign(row[6]);
      db->freeResult();
      string strtimeLimit="timeout "+timeLimit+"s ";
      //start timer
      gettimeofday(&begin, NULL);
      ret=system((strtimeLimit+runParam[sourceType]+" <../data/problems/TEST/input.in >/tmp/online_judge/output.out ").c_str());
      gettimeofday(&end, NULL);
      //end timer
      result=WEXITSTATUS(ret);
      timeElapsed=(end.tv_sec - begin.tv_sec)+(end.tv_usec-begin.tv_usec)/1000000.0;
      cout<<"timeElapsed: "<<timeElapsed<<endl;
      if(result!=0){
         error=true;
         if(result==124)
            result=3;
         else
            result=2;
      }
   }   
   void checkOutput()
   {
      if(error) return;
      string path="../data/problems/"+problemCode+"/output.out";
      string judgeOp=stringBuilder(path);
      path=workingDir+"output.out";
      string userOP=stringBuilder(path);
      if(judgeOp.compare(userOP)!=0)result=4;
      else result=5;
      
   }
   
   int getResultCode()
   {
      return result;
   }
   
   string getResult()
   {
      switch( result )
      {
         case 0:
            strResult =  "Successful";
            break;
            
         case 1:
            strResult = "CME";
         case 2:
            strResult = "RE";
            break;
         case 3:
            strResult="TLE";
            break;
         case 4:
            strResult = "WA";
            break;
         case 5:
            strResult="AC";
            break;
         default:
            strResult = "Unkown Result";
      }
      
      return strResult;
   }
};


int main(int argc, char *argv[])
{
   //freopen( "error.log", "w", stderr );
   if( argc < 2 )
   {
      cout << "Usage: ./jobcompiler jobid" << endl;
      return 1;
   }
   JobCompiler jc( argv[1] );
   jc.doWork();
   cout << jc.getResult() << endl;
   return 0;
}
