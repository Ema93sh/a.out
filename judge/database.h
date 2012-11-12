#include <iostream>
#include <string>
#include <my_global.h>
#include <mysql.h>

using namespace std;


class Database
{
	private:
		string username;
		string password;
		string hostname;
		string dbname;
		bool connected;
		MYSQL *conn;
		MYSQL_RES  *result;
		MYSQL_ROW row;
		string query;
		int num_fields;
	public:
		Database( string user, string pass )
		{
			username = user;
			password = pass;
			hostname = "localhost";
			dbname = "online_judge";
		}


		void error_handle(MYSQL *conn)
		{
			printf("Error %u: %s\n", mysql_errno(conn), mysql_error(conn));
		}
		
		void setLocalhost( string host )
		{  hostname = host; }

		void setDbname( string n )
		{ dbname = n; }

		bool initialize()
		{
			conn = mysql_init(NULL);
			if( conn == NULL )
			{
				error_handle(conn);
				return false;
			}
			return true;
		}

		bool connect()
		{
			if( mysql_real_connect(conn, hostname.c_str(), username.c_str(), password.c_str(), dbname.c_str(), 0, NULL, 0 ) == NULL)
			{
				connected = false;
				error_handle(conn);
			}
			else
				connected = true;
		
			return connected;
		}

		void query(string q)  // use it for simple query's like insert update etc . For queries that dont need stored result.
		{
			query = q;
			if( mysql_query( conn, query.c_str() ) != 0 ) error_handle();
		}

		void setQuery(string q)
		{
			query = q;
		}

		int useQuery() // returns the number of fields/cols
		{
			result = mysql_store_result(conn);
			num_fields = mysql_num_fields(result);
			return num_fiels;
		}

		MYSQL_ROW getRow()
		{
			return mysql_fetch_row(conn);
		}
};
