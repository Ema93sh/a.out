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
   const char *db_user="root",*db_password="password",*db_host="localhost",*db_name="daemoncheck";
   MYSQL *conn;
   MYSQL_RES *result;
   MYSQL_ROW row;
   char query[100];
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
      if(mysql_query(conn,"SELECT sub_id FROM job_queue LIMIT 1")!=0)
         error_handle(conn);
      result=mysql_store_result(conn);
      if(!(row=mysql_fetch_row(result))){
         printf("No submissions to be judged now\n");
         sleep(2);
      }else{
         //pass submission id to job_compiler
         char *sub_id=row[0];
         printf("Judging submission id: %s\n",sub_id);
         system("");
         sprintf(query,"DELETE FROM job_queue WHERE sub_id=%s",sub_id);
         if(mysql_query(conn,query)!=0)
            error_handle(conn);
      }
      mysql_free_result(result);
   }
   mysql_close(conn);
   return 0;
}