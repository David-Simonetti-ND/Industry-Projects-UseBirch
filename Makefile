all: master ex_prog1 ex_prog2
master: master.cpp
	g++ -std=c++11 -Wall master.cpp -o master
ex_prog1: ex_prog1.cpp
	g++ -std=c++11 -Wall -ggdb ex_prog1.cpp -o ex_prog1
ex_prog2: ex_prog2.cpp
	g++ -std=c++11 -Wall -ggdb ex_prog2.cpp -o ex_prog2