all: command test test2
command: command.cpp
	g++ -std=c++11 -Wall command.cpp -o command
test: test.cpp
	g++ -std=c++11 -Wall -ggdb test.cpp -o test
test2: test2.cpp
	g++ -std=c++11 -Wall -ggdb test2.cpp -o test2