all: parse
vector: vector.tab.c
	gcc vector.tab.c -o vector
vector.tab.c: vector.y globals.h
	bison --debug -t -d -Dparse.trace vector.y -o vector.tab.c
parse: parse.c vector.tab.c
	gcc vector.tab.c parse.c -o parse
parse.c: parse.l globals.h
	flex -t parse.l > parse.c
clean:
	rm parse vector.tab.c vector.tab.h vector.output parse.c