//g++ job_compiler.cpp `mysql_config --cflags --libs`

#include <iostream>
#include <string>
#include <my_global.h>
#include <mysql.h>
#include "DBconnect.h"
#include <map>
using namespace std;


/* Input: JobID
 *   Output: Result of compilation( CME, WA, TLE, RE, etc )
 *   for now assuming jobid is the filename of source program
 */

inline void error_handle(MYSQL *conn){
   printf("Error %u: %s\n", mysql_errno(conn), mysql_error(conn));
   exit(1);
}
MYSQL *conn;
class JobCompiler
{
private:
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
   int sourceType; // 1 - c , 2 - c++, 3 - python

public:
   string stringBuilder(string path){
      
   }
   JobCompiler( string jid )
   {
      srcType["C"]=1;
      srcType["CPP"]=2;
      srcType["Python"]=3;
      
      
      error = false;
      jobId = jid;
      result = 0;
      compileParam[1]="gcc -o output "+jobId+".c";
      compileParam[2]="g++ "+jobId+".cpp -o output";
      
      runParam[1]="./output";
      runParam[2]="./output";
      runParam[3]="python "+jobId+".py";
      
   }
   
   void doWork()
   {
      checkType();
   }
   
   void checkType()
   {
      MYSQL_RES *result;
      MYSQL_ROW row;
      str="SELECT * FROM submissions WHERE submissionId=\""+jobId+"\" LIMIT 1";
      if(mysql_query(conn,str.c_str())!=0)
         error_handle(conn);
      result=mysql_store_result(conn);
      row=mysql_fetch_row(result);
      lang.assign(row[2]);
      problemCode.assign(row[1]);
      sourceType=srcType[lang];
      mysql_free_result(result);
      //if it is an interpreted language call runIt
      //else call compileIt
      if(sourceType==1||sourceType==2)
         compileIt();
      else
         runIt();
   }
   
   void compileIt()
   {
      // need to check source code type
      result = system(compileParam[sourceType].c_str());
      if( result != 0 )
      {
         error = true;
         result = 1;
      }else{
         runIt();
      }
   }
   
   void runIt()
   {
      MYSQL_RES *result;
      MYSQL_ROW row;
      str="SELECT * FROM problems WHERE problemCode=\""+problemCode+"\" LIMIT 1";
      if(mysql_query(conn,str.c_str())!=0)
         error_handle(conn);
      result=mysql_store_result(conn);
      row=mysql_fetch_row(result);
      timeLimit.assign(row[5]);
      sourceLimit.assign(row[4]);
      memoryLimit.assign(row[6]);
      mysql_free_result(result);
      
      string strtimeLimit="timeout "+timeLimit+"s";
      if(error) return;
      //start timer
      result=system((strtimeLimit+runParam[sourceType]+" <../data/TEST/input.in >/tmp/online_judge/output.out ").c_str());
      //end timer
      if(result!=0){
         error=true;
         if(result==31744)//change it later,error code when tle my machine is weird
            result=3;
         else
            result=2;
      }else{
         checkOutput();
      }
   }
   
   void checkOutput()
   {
      if(error) return;
      string path="../../data/"+problemCode+"/output.out";
      string judgeOp=stringBuilder(path);
      path="/tmp/online_judge/output.out";
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
            break;
            
         case 2:
            strResult = "RE";
            break;
         case 3:
            strResult="TLE";
            break;
         default:
            strResult = "Unkown Result";
      }
      
      return strResult;
   }
};
int main(int argc, char *argv[])
{
   freopen( "error.log", "w", stderr );
   if( argc < 2 )
   {
      cout << "Usage: ./jobcompiler jobid" << endl;
      return 1;
   }
   
   
   //connect to db   
   conn=mysql_init(NULL);
   //connection variable
   if(conn == NULL){
      error_handle(conn);
   }
   //connect to mysql
   if(mysql_real_connect(conn, db_host, db_user, db_password, NULL, 0, NULL, 0) == NULL){
      error_handle(conn);
   }
   //select database
   if(mysql_select_db(conn,db_name)!=0){
      error_handle(conn);
   }
   //connection established
   
   
   
   JobCompiler jc( argv[1] );
   jc.doWork();
   cout << jc.getResult() << endl;
   
   return 0;
}
