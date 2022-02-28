SRC = test_programs
BIN = bin
PARSING = parsing
all: argument_test example map_test recursion var_test vector_test parse
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
vector: vector.tab.c
	gcc $(PARSING)/vector.tab.c -o $(PARSING)/vector
vector.tab.c: $(PARSING)/vector.y 
	bison --debug -t -d -Dparse.trace $(PARSING)/vector.y -o $(PARSING)/vector.tab.c
parse: $(PARSING)/parse.c vector.tab.c
	gcc $(PARSING)/vector.tab.c $(PARSING)/parse.c -o $(PARSING)/parse
parse.c: $(PARSING)/parse.l
	flex -t $(PARSING)/parse.l > $(PARSING)/parse.c
clean: 
	rm trace.json $(BIN)/argument_test $(BIN)/example $(BIN)/map_test $(BIN)/recursion $(BIN)/var_test $(BIN)/vector_test $(PARSING)/parse $(PARSING)/vector.tab.c $(PARSING)/vector.tab.h $(PARSING)/vector.output $(PARSING)/parse.c 