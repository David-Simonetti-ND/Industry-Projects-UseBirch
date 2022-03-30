#!/usr/bin/env python
from pygdbmi.gdbcontroller import GdbController
from pprint import pprint
import time, sys, json, os, ast
import re
import subprocess
import trace_vars
import trace_print

internal_trace_json = {} # used to hold trace.json
current_frame_number = 0 # current frame in the JSON
file_name = "" # file currently running
current_line = 0 # current line number in program
current_stdout = "" # what the current stdout is
current_stack_depth = 1 # counts how many recurisve function calls we are currently in - being in main counts as 1, so calling another function will make this 2
current_func_name = "" # name of the current function
line_next_to_execute = "" # line of c/c++ code that will be executed in the next step
local_variable_dictionary = {} # create a dictionary listing all local variables as keys with their value
return_value = None
args = {} # dictionary to hold function arguments
command_line_args = [] # list to hold any given command line arguments

def append_frame(): # call this function when all the global variables are up to date for the current frame, this will append the new frame
    global current_frame_number
    temp_dict = {}
    for key in local_variable_dictionary:
        temp_dict[key] = local_variable_dictionary[key]
    internal_trace_json["frame " + str(current_frame_number)] = \
    {"currentLine" : current_line, \
    "codeNextToRun" : line_next_to_execute, \
    "fileName" : file_name, \
    "commandLineArgs" : command_line_args, \
    "stdout" : current_stdout, \
    "stack" : {"numStackFrames" : current_stack_depth, \
    "topStackFrame" : {"methodName" : current_func_name, \
    "variables" : temp_dict },
    "returnValue" : return_value
        },
    "args" : args
    }
    current_frame_number += 1

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

command_line_arg_response = gdbmi.write('print *argv@argc')

if "No symbol" not in command_line_arg_response[1]['payload'] and len(command_line_arg_response[1]['payload'].split(',')) != 1:
    arg_list = command_line_arg_response[1]['payload'].split()[5::2]
    arg_list[-1] = arg_list[-1][:-1:]

    for arg in arg_list:
        command_line_args.append(''.join(filter(str.isalnum, arg)))

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
    
    try:
        response_args = response[-1]['payload']['frame']['args']
        for arg in response_args:
                args[arg['name']] = arg['value']
    except:
        pass

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
        curr_name = key
        val = define_val_type(val)
        try:
            if all_main_locals[key] != val:
                all_main_locals[key] = val
                local_variable_dictionary[key] = val
        except:
            continue

    append_frame() # create new stack frame

    # Reset values
    return_value = None
    args = {}
    print(f"Executed line {current_line}")

    if "return" in line_next_to_execute and "main" in current_func_name:
        gdbmi.exit()
        break

# output the trace.json from internal_trace_json
output.close()
os.remove("output.txt")
out_file = open("trace.json", "w")
json.dump(internal_trace_json, out_file, indent = 6)
out_file.close()