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
   	while(true)
   	{

   	   db.setQuery(string("SELECT submission_id FROM jobQueue LIMIT 1"));
     	   db.useQuery();
      	   if(!(row=db.getRow()))
           {
             //printf("No submissions to be judged now\n"); maybe uncomment later
             sleep(1);
           }
           else
           {
             //pass submission id to job_compiler
             string subId;
             subId.assign(row[0]);
             char st[200];
             cout<< "Judging submission id:" << subId << endl;
             system("g++ job_compiler.cpp `mysql_config --cflags --libs` -o jobCompiler"); // need to remove this later
             sprintf(st,"./jobCompiler %s",subId.c_str());
             system(st);
             db.simpleQuery(string("DELETE FROM jobQueue WHERE submission_id="+subId));
	   }

      db.freeResult();
      //break;
   }
   return 0;
}
