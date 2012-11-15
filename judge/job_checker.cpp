//g++ job_checker.cpp `mysql_config --cflags --libs`
#include <iostream>
#include <fstream>
#include <cstdio>
#include <string>
#include "database.h"
using namespace std;

int main()
{
	Database db;
	db.initialize();
	db.connect();
   	int num_row;  
	MYSQL_ROW row;

	ofstream log;
	log.open("log.txt", ios::app );

   	while(true)
   	{

   	   db.setQuery(string("SELECT submissionId FROM jobQueue LIMIT 1"));
     	   db.useQuery();
      	   if(!(row=db.getRow()))
           {
             printf("No submissions to be judged now\n");
             sleep(2);
           }
           else
           {
             //pass submission id to job_compiler
             char *subId=row[0];
	     char st[100];
             log << "Judging submission id:" << subId << endl;
             system("g++ job_compiler.cpp `mysql_config --cflags --libs` -o jobCompiler"); // need to remove this later
             sprintf(st,"./jobCompiler %s",subId);
             system(st);
             
		 /*sprintf(st,"DELETE FROM jobQueue WHERE submissionId=%s",subId);
      	 	  if(mysql_query(conn,st)!=0)
       	     	error_handle(conn);
       			  */
       	       /*sprintf(st,"UPDATE submissions SET status=\"waiting\" WHERE submissionId=%s",subId);
        	 if(mysql_query(conn,st)!=0)
        	    error_handle(conn);
        	 */
          }
      db.freeResult();
      break;
   }
   return 0;
}
