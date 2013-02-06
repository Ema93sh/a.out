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
   try{ 
      db.connect();
   }catch (string ex){
      printf ("%s\n",ex.c_str());
   }
   int num_row;  
   MYSQL_ROW row;
   system("mkdir -p environment");
   system("mkdir -p cache");
   while(true)
   {
      try{
         db.setQuery(string("SELECT submission_id FROM jobQueue LIMIT 1"));
         db.useQuery();
         if(!(row=db.getRow()))
         {
            printf("Judge is online and no submissions to be judged now\n"); //maybe uncomment later
            sleep(2);
         }
         else
         {
            //pass submission id to job_compiler
            string subId;
            subId.assign(row[0]);
            char st[200];
            db.simpleQuery(string("DELETE FROM jobQueue WHERE submission_id="+subId));
            
            cout<< "Judging submission id:" << subId << endl;
            //system("g++ jobCompiler.cpp base64.o `mysql_config --cflags --libs` -o jobCompiler "); // need to remove this later
            sprintf(st,"./jobCompiler %s",subId.c_str());
            system(st);
         }
      }catch (string ex){
         printf("%s\nretrying\n\n\n",ex.c_str());
         sleep(2);
         try{
           db.connect();
         } catch (string s){ 
            printf("%s",s.c_str());
         }
      }
   }
   db.freeResult();
   //break;
   return 0;
}
