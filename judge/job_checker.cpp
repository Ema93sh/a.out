//g++ job_checker.cpp `mysql_config --cflags --libs`

#include<stdio.h>
#include<mysql.h>
#include <my_global.h>
#include "DBconnect.h"
using namespace std;

inline void error_handle(MYSQL *conn){
   printf("Error %u: %s\n", mysql_errno(conn), mysql_error(conn));
   exit(1);
}

int main(){
   //useful variables
   MYSQL *conn;
   MYSQL_RES *result;
   MYSQL_ROW row;
   char st[100];
   int num_row;
   
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
   
   while(true){
      if(mysql_query(conn,"SELECT submissionId FROM jobQueue LIMIT 1")!=0)
         error_handle(conn);
      result=mysql_store_result(conn);
      if(!(row=mysql_fetch_row(result))){
         printf("No submissions to be judged now\n");
         sleep(2);
      }else{
         //pass submission id to job_compiler
         char *subId=row[0];
         printf("Judging submission id: %s\n",subId);
         system("g++ job_compiler.cpp `mysql_config --cflags --libs` -o jobCompiler");
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
      mysql_free_result(result);
      break;
   }
   mysql_close(conn);
   return 0;
}