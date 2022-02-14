all: master ex_prog1 ex_prog2 automated example
master: master.cpp
	g++ -std=c++11 -Wall master.cpp -o master
automated: automated.cpp
	g++ -std=c++11 -Wall automated.cpp -o automated
ex_prog1: ex_prog1.cpp
	g++ -std=c++11 -Wall -ggdb ex_prog1.cpp -o ex_prog1
ex_prog2: ex_prog2.cpp
	g++ -std=c++11 -Wall -ggdb ex_prog2.cpp -o ex_prog2
example: example.cpp
	g++ -std=c++11 -Wall -ggdb example.cpp -o example
recursion: recursion.cpp
	g++ -std=c++11 -Wall -ggdb recursion.cpp -o recursion
clean: 
	rm master ex_prog1 ex_prog2 automated example recursion trace.json