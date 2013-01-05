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
   string jobId;
   bool error; 
   string timeLimit,sourceLimit,memoryLimit;
   string sampleInputPath;
   string sampleOutputPath;
   string sourcePath;
   string path;
   string compileParam;
   int result; // 0 - success, 1 - CME , 2 - RE, 3 - TLE, 4 - WA ,5 - AC
   string strResult; // converted result code to string
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
      path = "/Learning/Projects/GIT/a.out/";
      jobId = jid;
      error = false;
      result = 0;
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
      updateResult();
   }
   
   void checkType()
   {
      string str;
      MYSQL_ROW row;
      str="SELECT language_id, problem_id, userCode FROM submissions WHERE id= "+jobId+" LIMIT 1";
      db->setQuery(str);
      db->useQuery();
      row= db->getRow();
      string langid;
      langid.assign( row[0] );
      string probid;
      probid.assign( row[1] );
      sourcePath.assign( row[2] );
      db->freeResult();
      
      str ="SELECT inputFile, outputFile, sourceLimit, timeLimit, memoryLimit FROM problems WHERE id="+probid+" LIMIT 1";
      db->setQuery(str);
      db->useQuery();
      row = db->getRow();

      sampleInputPath = row[0];
      sampleOutputPath = row[1];
      sourceLimit = row[2];
      timeLimit = row[3];
      memoryLimit = row[4];
      db->freeResult();

      str = "SELECT compileParam FROM language WHERE id="+langid+" LIMIT 1";
      db->setQuery(str);
      db->useQuery();
      row = db->getRow();
      
      compileParam = row[0];
      db->freeResult();

      //if it is an interpreted language call runIt
      //else call compileIt
   }
   
   void compileIt()
   {
     sourcePath = path + "data/" + sourcePath;
     string final = compileParam + " " + sourcePath;
     cout << "compiling: " << final << endl;
     result = system(final.c_str());

      if( result != 0 )
      {
	 cout << "Error While compiling" << endl;
         error = true;
         result = 1;
      }
   }   
   void runIt()
   {
      if(error)return;
      int ret;
      struct timeval begin, end; //for calculating time elapsed
      string strtimeLimit="timeout "+timeLimit+"s ";
      //start timer
      sampleInputPath = path + "data/" + sampleInputPath;
      string final = string("./a.out ") + "< " + sampleInputPath + " > " + "output"; 
      cout << "running: " << final << endl;
      gettimeofday(&begin, NULL);
      ret=system(final.c_str());
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

      sampleOutputPath = path + "data/" + sampleOutputPath;
      cout << "Sample Output:" << sampleOutputPath << endl; 
      string judgeOp=stringBuilder(sampleOutputPath);
      string temp = path + "/judge/output";
      cout << "Current Output:" << temp << endl;
      string userOP=stringBuilder(temp);
      if(judgeOp.compare(userOP)!=0)result=4;
      else result=5;
   }

   void updateResult()
   {
	   string result = getResult();
	   string query = "UPDATE submissions SET status =\"" + result +"\" WHERE id =" +jobId;
	   cout << "Update: " << query <<  endl;
	   db->simpleQuery(query);
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
            strResult =  "ERR";
            break;

         case 1:
            strResult = "CTE";
         case 2:
            strResult = "RTE";
            break;
         case 3:
            strResult="TLE";
            break;
         case 4:
            strResult = "WRA";
            break;
         case 5:
            strResult="ACC";
            break;
         default:
            strResult = "ERR";
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
