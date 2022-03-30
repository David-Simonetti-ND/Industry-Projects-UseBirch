SRC = test_programs
BIN = bin
PARSING = parsing
all: bin test_program parse
bin:
	mkdir bin
test_program:
	cd test_programs && $(MAKE) 
parse:
	cd parsing && $(MAKE) 
update_gdb:
	cp gdbcontroller.py ~/miniconda3/envs/UseBirch/lib/python3.10/site-packages/pygdbmi/gdbcontroller.py
	cp .gdbpoint ~/.gdbinit
clean: 
	cd test_programs && $(MAKE) clean
	cd parsing && $(MAKE) clean
	rm trace.json output.txt  myinput.in