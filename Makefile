SRC = test_programs
BIN = bin
all: argument_test example map_test recursion var_test vector_test
argument_test: $(SRC)/argument_test.cpp
	g++ -std=c++11 -Wall -ggdb $(SRC)/argument_test.cpp -o $(BIN)/argument_test
example: $(SRC)/example.cpp
	g++ -std=c++11 -Wall -ggdb $(SRC)/example.cpp -o $(BIN)/example
map_test: $(SRC)/map_test.cpp
	g++ -std=c++11 -Wall -ggdb $(SRC)/map_test.cpp -o $(BIN)/map_test
recursion: $(SRC)/recursion.cpp
	g++ -std=c++11 -Wall -ggdb $(SRC)/recursion.cpp -o $(BIN)/recursion
var_test: $(SRC)/var_test.cpp
	g++ -std=c++11 -Wall -ggdb $(SRC)/var_test.cpp -o $(BIN)/var_test
vector_test: $(SRC)/vector_test.cpp
	g++ -std=c++11 -Wall -ggdb $(SRC)/vector_test.cpp -o $(BIN)/vector_test
update_gdb:
	cp gdbcontroller.py ~/miniconda3/envs/UseBirch/lib/python3.10/site-packages/pygdbmi/gdbcontroller.py
	cp .gdbpoint ~/.gdbinit
clean: 
	rm trace.json $(BIN)/argument_test $(BIN)/example $(BIN)/map_test $(BIN)/recursion $(BIN)/var_test $(BIN)/vector_test 