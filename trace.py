#!/usr/bin/env python
from pygdbmi.gdbcontroller import GdbController
from pprint import pprint
import time, sys, json, os
# how to run program: once your conda environment is initialized, run ./trace.py with the first argument being the executable you wish to run
# ex. ./trace.py example
# output will appear in trace.json
# general overview of program:
# The goal is to create a trace.json file, which is made up of a JSON consisting of a list of all stack frames
# where a stack frame is basically taking a snapshot of the current state of the program
# (e.g. you want to know the state of variables, what line we're on, what function we're in, etc)
# the trace.json is stored in internal_trace_json which is just output to a file when the program runs
# so, how do we do this?
# we have a bunch of global variables (the ones listed below) which keep track of their respective element of the program state
# so once these variables are updated to be correct for the given stack frame, the append_frame function can be called
# and it basically creates a new entry in the internal_trace_json file holding the information about the frame
# so the basic program flow looks like this
# write to gdb saying to execute another line -> get output from gdb -> parse output to get info about current frame -> update global variables which hold onto info about the frame -> append the frame to the internal_trace_json with append_frame()
internal_trace_json = {} # used to hold trace.json
current_frame_number = 0 # keep track of which frame we are on
file_name = "" # what is the file we are running
current_line = 0 # what line number we're on
current_stdout = "" # what the current stdout is
current_stack_depth = 1 # counts how many recurisve function calls we are currently in - being in main counts as 1, so calling another function will make this 2
current_func_name = "" # name of the function we are currently in
line_next_to_execute = "" # line of c/c++ code that will be executed in the next step
local_variable_dictionary = {} # create a dictionary listing all local variables as keys with their value
return_value = None
def append_frame(): # call this function when all the global variables are up to date for the current frame, this will append the new frame
    global current_frame_number
    temp_dict = {}
    for key in local_variable_dictionary:
        temp_dict[key] = local_variable_dictionary[key]
    internal_trace_json["frame " + str(current_frame_number)] = \
    {"currentLine" : current_line, \
    "codeNextToRun" : line_next_to_execute, \
    "fileName" : file_name, \
    "stdout" : current_stdout, \
    "stack" : {"numStackFrames" : current_stack_depth, \
    "topStackFrame" : {"methodName" : current_func_name, \
    "variables" : temp_dict },
    "returnValue" : return_value
    } }
    current_frame_number += 1
def print_frame_json(): # used to debug and print out all the frames currently in internal_trace_json
    pprint(internal_trace_json["frame " + str(current_frame_number - 1)])
punctMap = { # Only the braces in this map are used as of now. This is here so that if gdb returns a similar syntax for vectors or maps, adding them to the variable dictionary is easier
    '{': '}',
    '[': ']',
    '(': ')',
}
def define_val_type(val): # recursive function used to change strings into typed variables
    val = val.strip("\\n")
    val = val.lstrip()
    # process Booleans
    if val == 'true':
        return bool(True)
    if val == 'false':
        return bool(False)
    # process Integers
    try:
        return int(val)
    except:
        pass
    # process Doubles and Floats
    try:
        return float(val)
    except:
        pass
    # process mapsgit 
    if "std::map" in val:
        print("MAP!")
        map = {}
        try: 
            val = val.split('{')[1].split('}')[0]
        except:
            return val
        items = val.split(',')
        for item in items:
            (key, value) = item.split(" = ")
            key = key.split('[')[1].split(']')[0]
            map[define_val_type(key)] = define_val_type(value)
        return map
    # process List-Type variables              
    if (val[0] == '{') or (val[0] == '[') or (val[0] == '('):
        end_punct = punctMap[val[0]]
        tempList = []
        val = val.lstrip()
        val = val[1:-1] # Remove first brace
        splitchar = ","
        if f"{end_punct}," in val:
            val = val.replace(f"{end_punct},", f"{end_punct}|")
            splitchar = "|"
        for item in val.split(splitchar):
            if item == '':
                continue
            tempList.append(define_val_type(item))
        return tempList
    return val
# Open file that will hold stdout of gdb
output = open("output.txt", "w+")
# Start gdb process
gdbmi = GdbController()
# Load binary passed in argv[1] and check we only have one arg
if len(sys.argv) < 2:
    print("Please pass in at least one argument (executable you wish to run)!")
    exit()
gdbmi.write(f'-file-exec-file {sys.argv[1]}')
# load symbols from the executable
gdbmi.write(f'file {sys.argv[1]}')
gdbmi.write('skip -gfi /usr/include/c++/4.8.2/bits/*.h')
gdbmi.write('skip -gfi /usr/include/c++/9/bits/*.h')
# write command line arguments if neeeded
if (len(sys.argv) != 2):
    # start running the program and capture the output in response
    response = gdbmi.write("start " + " ".join(sys.argv[2:]) + " >> output.txt")
else:
     response = gdbmi.write("start >> output.txt")
# these lines below break down the output
current_func_name = response[2]['payload']['bkpt']['func'] # gather current function name (should be main but why not be safe)
file_name = response[2]['payload']['bkpt']['file'] # gather file name
unprocesses_gdb_line = "" # holds lines of interest
for line_of_gdb_output in response: # loop through output and look for lines where gdb sends something to the console
    if line_of_gdb_output['type'] == 'console': # do something if we find console out
        unprocesses_gdb_line = line_of_gdb_output['payload'].strip("\\n") # this contains info about the line being executed
        strip_index = unprocesses_gdb_line.find("\\t") # and try to find a tab
        if (strip_index == -1): # function call - do nothing
            continue
        if "}" in unprocesses_gdb_line and "{" not in unprocesses_gdb_line: # return from function call - act accordingly
            current_line = unprocesses_gdb_line[:strip_index]
            line_next_to_execute = "return from " + current_func_name
            continue
        # otherwise we got a regular line
        current_line = unprocesses_gdb_line[:strip_index].rstrip() # get the line number
        line_next_to_execute = unprocesses_gdb_line[strip_index + 2:].lstrip() # and the line about to be executed
response = gdbmi.write('info locals') # get info about local vars
# parse through the response (variables are output with a lot of newlines, very messy)
# put it together into one string to be manipulated
all_main_locals = {}
for i in range(1, len(response) - 1):
    try:
        (key, val) = response[i]['payload'].split(" = ", 1)
    except:
        continue
    val = define_val_type(val)
    all_main_locals[key] = val
append_frame()
while True: # infinite loop until we reach the end
    response = gdbmi.write('step') # send GDB to execute one line
    gdbmi.write('call ((void(*)(int))fflush)(0)') # flush any stdout that is in the buffer to wherever stdout is directed to
    if len(response) < 4:
        continue
    if ("__libc_start_main" in response[3]['payload']): # this checks for when we reach the end
        gdbmi.exit()
        break
    unprocesses_gdb_line = "" # holds lines of interest
    for line_of_gdb_output in response: # loop through output and look for lines where gdb sends something to the console
        if line_of_gdb_output['type'] == 'console': # do something if we find console out
            unprocesses_gdb_line = line_of_gdb_output['payload'].strip("\\n") # this contains info about the line being executed
            strip_index = unprocesses_gdb_line.find("\\t") # and try to find a tab
            if (strip_index == -1): # function call - do nothing
                continue
            if "}" in unprocesses_gdb_line and "{" not in unprocesses_gdb_line: # return from function call - act accordingly
                current_line = unprocesses_gdb_line[:strip_index]
                line_next_to_execute = "return from " + current_func_name
                raw_return = gdbmi.write("print $eax")[1]['payload'].split("=")[1]
                raw_return = raw_return.lstrip()
                return_value = raw_return.strip("\\n")
                continue
            # otherwise we got a regular line
            current_line = unprocesses_gdb_line[:strip_index].rstrip() # get the line number
            line_next_to_execute = unprocesses_gdb_line[strip_index + 2:].lstrip() # and the line about to be executed
    if os.path.getsize("output.txt") > 0: # if condition to read any stdout that was redirected to the output.txt file
        try:
            current_stdout = ''.join(output.readlines())
        except:
            continue
    else:
        current_stdout = ""
    raw_stack = gdbmi.write('bt') # this sends the back trace command - basically lists the current function call trace
    current_func_name = raw_stack[1]['payload'].split(" ")[2] + "()" # get the current name of the function we are in
    current_stack_depth = len(raw_stack) - 2 # and calculate how many function calls deep we are based on the length of the response
    response = gdbmi.write('info locals') # get info about local vars - similar to how it was done above
    for i in range(1, len(response) - 1):
        try:
                (key, val) = response[i]['payload'].split(" = ", 1)
        except:
            continue
        val = define_val_type(val)
        try:
            if all_main_locals[key] != val:
                all_main_locals[key] = val
                local_variable_dictionary[key] = val
        except:
            continue
    append_frame() # create new stack frame
    return_value = None
    print(f"Executed line {current_line}")
# output the trace.json from internal_trace_json
output.close()
os.remove("output.txt")
out_file = open("trace.json", "w")
json.dump(internal_trace_json, out_file, indent = 6)
out_file.close()