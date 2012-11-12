//g++ job_compiler.cpp `mysql_config --cflags --libs`

#include <iostream>
#include <string>
#include <my_global.h>
#include <mysql.h>
#include "DBconnect.h"
using namespace std;


/* Input: JobID
 *   Output: Result of compilation( CME, WA, TLE, RE, etc )
 *   for now assuming jobid is the filename of source program
 */

inline void error_handle(MYSQL *conn){
   printf("Error %u: %s\n", mysql_errno(conn), mysql_error(conn));
   exit(1);
}

class JobCompiler
{
private:
   string jobId;
   bool error; 
   int result; // 0 - success, 1 - CME , 2 - RE, 3 - TLE, 4 - WA
   string strResult; // converted result code to string
   int sourceType; // 1 - c , 2 - c++, 3 - python
public:
   JobCompiler( string jid )
   {
      error = false;
      jobId = jid;
      result = 0;
      
      // testing
      sourceType = 1;
   }
   
   void doWork()
   {
      checkType();
      compileIt();
      runIt();
      checkWithInput();
   }
   
   void checkType()
   {
      // later
   }
   
   void compileIt()
   {
      // need to check source code type
      switch(sourceType)
      {
         case 1:
         {
            string compiler = "g++ ";
            string arguments = " "; // send arguments to the compiler
            string output = "-o output "; // instead we need to add only jobid with out extension
            string f =  compiler + " " + arguments + output + jobId;
            result = system(f.c_str());
         }
         break;
         
         default:
            cout << "Unknown Source Type" << endl;
      }
      
      if( result != 0 )
      {
         error = true;
         result = 1;
      }
   }
   
   void runIt()
   {
      if(error) return;
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
   if( argc < 2 )
   {
      cout << "Usage: ./jobcompiler jobid" << endl;
      return 1;
   }
   
   
   //connect to db
   MYSQL *conn;
   
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
