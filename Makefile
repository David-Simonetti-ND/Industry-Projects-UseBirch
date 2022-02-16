all: master ex_prog1 ex_prog2 automated example argument_test recursion map
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
argument_test: argument_test.cpp
	g++ -std=c++11 -Wall -ggdb argument_test.cpp -o argument_test
map: map.cpp
	g++ -std=c++11 -Wall -ggdb map.cpp -o map
update_gdb:
	cp gdbcontroller.py ~/miniconda3/envs/UseBirchEnv/lib/python3.10/site-packages/pygdbmi/gdbcontroller.py
clean: 
	rm master ex_prog1 ex_prog2 automated example recursion trace.json argument_test map