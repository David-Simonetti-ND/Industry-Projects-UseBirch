SRC = test_programs
BIN = bin
PARSING = parsing
all: bin test_program parse
bin:
	mkdir bin
test_program:
	cd test_programs && $(MAKE) all
parse:
	cd parsing && $(MAKE) all
update_gdb:
	cp gdbcontroller.py ~/miniconda3/envs/UseBirch/lib/python3.10/site-packages/pygdbmi/gdbcontroller.py
	cp .gdbpoint ~/.gdbinit
clean: clean_parsing clean_test  
	rm trace.json output.txt  myinput.in
clean_test:
	cd test_programs && $(MAKE) clean
clean_parsing:
	cd parsing && $(MAKE) clean
	