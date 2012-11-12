#include <iostream>
#include <string>

using namespace std;


/* Input: JobID
   Output: Result of compilation( CME, WA, TLE, RE, etc )
   for now assuming jobid is the filename of source program
 */


class JobCompiler
{
	private:
	
		string jobId;
		bool error; 
		int result; // 0 - success, 1 - CME , 2 - RE, 3 - TLE, 4 - WA
		string strResult; // convierted result code to string
		int sourceType; // 1 - c , 2 - c++, 3 - python
		string errorMsg; // If an error has occured. Then this variable will hold the error msg
	
	  
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

		void checkWithTestCases()
		{
			if(error) return;
		}

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
			checkWithTestCases();
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

	JobCompiler jc( argv[1] );
	jc.doWork();
	cout << jc.getResult() << endl;

	return 0;
}
