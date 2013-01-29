#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <cstdlib>
#include <vector>
#include <cmath>
#include "base64.h"
#include "database.h"


using namespace std;

class JobCompiler
{
  private:
    Database db;
    string path, sourcePath;
    string submissionId, problemId, languageId, codeId;
    string timeLimit, memoryLimit, sourceLimit;
    double timeElapsed, memElapsed,allowedError;
    string compileParam;
    bool error, isCompiled,decimalJudge;
    int result, noOfTestCases;
  public:
    JobCompiler( string subid ): db()
  {
    //path = "/Learning/Projects/GIT/a.out/";
    path = "/home/vinith/GIT/a.out/";
    submissionId = subid;
    result = 0;
    error = false;
    db.initialize();
    db.connect();
  }

    vector<string> vectorBuilder(string path){
      ifstream fin(path.c_str());
      string s;
      vector<string> ret(1000);
      while(fin>>s)ret.push_back(s);
      fin.close();
      return ret;
    }
    bool isDecimal(string s){
      int dotcount=0,l=s.length();
      bool valid=true;
      for(int i=0;i<l;i++){
        if(s[i]=='.')dotcount++;
        else if(!(s[i]>='0'&&s[i]<='9')){
          valid=false;
          break;
        }
      }
      if(valid&&dotcount<2)return true;
      return false;
    }
    void doWork()
    {
      checkType();
      compileIt();
      runIt();
      updateResult();
    }

    void checkType()
    {
      MYSQL_ROW row;
      string str;
      // get Submission Info
      cout << "Getting Submission Info from db..." << endl;
      str = "SELECT language_id, problem_id, userCode FROM submissions WHERE id = " + submissionId + " LIMIT 1";
      cout << str << endl;
      db.setQuery(str);
      db.useQuery();
      row = db.getRow();

      languageId.assign( row[0] );
      problemId.assign( row[1] );
      codeId.assign( row[2] );
      db.freeResult();

      // get Problem Info
      cout << "Getting Problem Info from db...id = " << problemId << " "<< endl;
      str = "SELECT sourceLimit, timeLimit, memoryLimit,decimalJudgeOn,absoluteError FROM problems WHERE id = " + problemId;
      cout << str << endl;
      db.setQuery( str );
      db.useQuery();
      row = db.getRow();

      sourceLimit.assign( row[0] );
      timeLimit.assign( row[1] );
      memoryLimit.assign( row[2] );
      if(row[3][0]=='1'){
        decimalJudge=true;
        allowedError=atof(row[4]);
      }
      db.freeResult();

      //get compile Parameters
      string extension;
      cout << "Getting the compile parameters from db..." << endl;
      str = "SELECT compileParam, langType, extension FROM language WHERE id = "+ languageId;
      cout << str << endl;
      db.setQuery( str );

      db.useQuery();
      row = db.getRow();

      compileParam.assign( row[0] );
      string t = row[1];
      extension.assign( row[2] );
      db.freeResult();
      if( t.compare("1")  == 0)
        isCompiled = true;
      else
        isCompiled = false;

      //create the source code file
      string sourceCode;
      cout << "Getting source code from db.." << endl;
      str = "SELECT content FROM database_files_file WHERE id ="+ codeId;
      cout << str << endl;
      db.setQuery( str );
      db.useQuery();
      row = db.getRow();

      sourceCode.assign( row[0] );
      db.freeResult();

      sourcePath = "environment/source"+extension;
      sourceCode = base64_decode( sourceCode );
      cout << "Source Code: " << endl << sourceCode << endl;

      ofstream sfile(sourcePath.c_str());
      sfile << sourceCode;
      sfile.close();
    }

    void compileIt()
    {
      if( isCompiled )
      {
        string final = compileParam + " " + sourcePath + " -o environment/executable";
        cout << "compiling: " << final << endl;
        result = system(final.c_str());
        if( result != 0 )
        {
          cout << "Error While compiling" << endl;
          error = true;
          result = 1;
        }
      }
    }
    void runIt()
    {
      if(error) return;

      // create all the input and output files files
      string str = "SELECT input, output FROM testcase WHERE problem_id = "+ problemId;
      cout << str << endl;
      MYSQL_ROW row;
      db.setQuery( str );
      db.useQuery();
      int k = 0;
      noOfTestCases = db.noOfRows();
      cout << "No of testCases = " << noOfTestCases << endl;
      int fileIds[noOfTestCases][2];
      for( int i = 0; i < noOfTestCases; i++)
      {
        row = db.getRow();
        fileIds[i][0] = atoi(row[0]);
        fileIds[i][1] = atoi(row[1]);
      }
      db.freeResult();

      stringstream out;
      out << "SELECT content FROM database_files_file WHERE id IN ( ";
      for( int i = 0; i < noOfTestCases; i++)
      {
        //cout << "TestCase "<< i <<":"<< endl;
        //cout << "i:" << fileIds[i][0] << " "
        //     << "o:" << fileIds[i][1] << endl;
        out << fileIds[i][0] << ", " << fileIds[i][1] << ", "; 
      }
      str = out.str();
      unsigned found = str.find_last_of(",");
      str[found] = ' ';
      str[found+1] = ')';
      cout << str << endl;
      db.setQuery(str);
      db.useQuery();

      for( int i=0; i < noOfTestCases; i++ )
      {

        string c, filename;
        //input file
        row = db.getRow();
        c.assign( row[0] );
        c = base64_decode(c);
        out.str( string() );
        //out << "environment/input" << i;
        filename = out.str();
        //cout << "Creating file " << filename << " with contents:"<< endl << c << endl;
        ofstream file( filename.c_str() );
        file << c;
        file.close();

        //output file
        row = db.getRow();
        c.assign( row[0] );
        c = base64_decode(c);
        out.str( string() );
        //out << "environment/output" << i;
        filename = out.str();
        //cout << "Creating file " << filename << " with contents"<< endl << c << endl;
        file.open( filename.c_str() );
        file << c;
        file.close();
      }

      // run the code
      int ret;
      struct timeval begin, end; //for calculating time elapsed
      string strtimeLimit="timeout "+timeLimit+"s ";
      string final ="";

      for( int i=0; i < noOfTestCases; i++ )
      {
        if( error) break;
        out.str( string() );
        out << "environment/input" << i;
        string input = out.str();

        out.str( string() );
        out << "environment/output" << i;
        string output = out.str();

        out.str( string() );
        out << "environment/user_output" << i;
        string user_output = out.str();

        if(isCompiled)
          final = string(" environment/./executable ") + "< " + input + " > " + user_output;
        else
          final = strtimeLimit + compileParam + " " +  sourcePath + " < " + input + " > " + user_output;

        cout << "Running TestCase " << i+1 << ": " << final << endl;

        //start timer
        gettimeofday(&begin, NULL);
        ret=system(final.c_str());
        gettimeofday(&end, NULL);
        //end timer
        result=WEXITSTATUS(ret);
        timeElapsed=(end.tv_sec - begin.tv_sec)+(end.tv_usec-begin.tv_usec)/1000000.0;
        cout<<"timeElapsed: "<<timeElapsed<<endl;
        if(result!=0)
        {
          error=true;
          if(result==124)
            result=3;
          else
            result=2;
        }

        cout<< "Checking output.." << endl;
        checkOutput(  output , user_output );
        cout << endl << endl;
      }
    }

    void checkOutput(string output, string user_output)
    {
      if(error) return;
      bool correct=true;
      double n1,n2;
      cout << "Sample Output:" << output << endl; 
      vector<string> judgeOp=vectorBuilder(output);
      cout << "User Output:" << user_output << endl;
      vector<string> userOP=vectorBuilder(user_output);
      if(judgeOp.size()!=userOP.size()){
        correct=false;
      }
      if(correct){
        vector<string>::iterator it1,it2;
        for(it1=judgeOp.begin(),it2=userOP.begin();it1!=judgeOp.end();it1++,it2++){
          if(!decimalJudge){
            if((*it1).compare(*it2)){
              correct=false;
              break;
            }
          }else{
            if(isDecimal(*it1)&&isDecimal(*it2)){
              n1=atof((*it1).c_str());
              n2=atof((*it2).c_str());
              if(fabs(n1-n2)>allowedError){
                correct=false;
                break;
              }
            }else{
              if((*it1).compare(*it2)){
                correct=false;
                break;
              }
            }
          }
        }
      }
      if(!correct)
      {
        result=4;
        error = true;
        cout << "Failed" << endl;
      }
      else 
      {
        result=5;
        cout << "Success" << endl;
      }
    }

    void updateResult()
    {
      string result = getResult();
      string query = "UPDATE submissions SET status =\"" + result +"\" WHERE id =" +submissionId;
      cout << "Update: " << query <<  endl;
      db.simpleQuery(query);
    }

    int getResultCode()
    {
      return result;
    }

    string getResult()
    {
      string strResult;
      switch( result )
      {
        case 0:
          strResult =  "ERR";
          break;

        case 1:
          strResult = "CTE";
          break;

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
  if( argc < 2 )
  {
    cout << "Usage: ./jobcompiler jobid" << endl;
    return 1;
  }
  JobCompiler jc( argv[1] );
  jc.doWork();
  //cout << jc.getResult() << endl;
  return 0;
}

