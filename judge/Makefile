
all: jobCompiler.o
	g++ jobChecker.cpp `mysql_config --cflags --libs` -o jobChecker

jobCompiler.o: base64.o
	g++ jobCompiler.cpp base64.o `mysql_config --cflags --libs` -o jobCompiler

base64.o:
	g++ -c base64.cpp

clean:
	rm *.o
