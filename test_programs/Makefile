BIN = bin
all: argument_test example map_test recursion var_test vector_test containers
argument_test: argument_test.cpp
	g++ -std=c++11 -Wall -ggdb argument_test.cpp -o ../$(BIN)/argument_test
example: example.cpp
	g++ -std=c++11 -Wall -ggdb example.cpp -o ../$(BIN)/example
map_test: map_test.cpp
	g++ -std=c++11 -Wall -ggdb map_test.cpp -o ../$(BIN)/map_test
recursion: recursion.cpp
	g++ -std=c++11 -Wall -ggdb recursion.cpp -o ../$(BIN)/recursion
var_test: var_test.cpp
	g++ -std=c++11 -Wall -ggdb var_test.cpp -o ../$(BIN)/var_test
vector_test: vector_test.cpp
	g++ -std=c++11 -Wall -ggdb vector_test.cpp -o ../$(BIN)/vector_test
containers: containers.cpp
	g++ -std=c++11 -Wall -ggdb containers.cpp -o ../$(BIN)/containers
clean:
	rm ../$(BIN)/argument_test ../$(BIN)/example ../$(BIN)/map_test ../$(BIN)/recursion ../$(BIN)/var_test ../$(BIN)/vector_test