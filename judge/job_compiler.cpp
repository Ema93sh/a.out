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
   int result; // 0 - success, 1 - CME , 2 - RE, 3 - TLE, 4 - WA
   string strResult; // converted result code to string
   map<string,int> srcType; // maps sourceType
   map<int,string> compileParam;//maps sourceType to compile parameters
   map<int,string> runParam;
   int sourceType; // 1 - c , 2 - c++, 3 - python
public:
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
      checkWithInput();
   }
   
   void checkType()
   {
      MYSQL_RES *result;
      MYSQL_ROW row;
      str="SELECT language FROM submissions WHERE submissionId=\""+jobId+"\" LIMIT 1";
      if(mysql_query(conn,str.c_str())!=0)
         error_handle(conn);
      result=mysql_store_result(conn);
      row=mysql_fetch_row(result);
      lang.assign(row[0]);
      sourceType=srcType[lang];
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
      if(error) return;
      //start timer
      //pipe the input file
      result=system((runParam[sourceType]+">output.txt ").c_str());
      //end timer
      if(result!=0){
         error=true;
         result=2;
      }
   }
   
   void checkWithInput()
   {
      if(error) return;
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
