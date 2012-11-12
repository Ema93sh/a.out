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

		void setQuery(string q)
		{
			query = q;
		}

};
