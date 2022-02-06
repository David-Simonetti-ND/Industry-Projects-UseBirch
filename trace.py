#!/usr/bin/env python
from curses import raw
from pygdbmi.gdbcontroller import GdbController
from pprint import pprint
import time, sys, json

frame_json = {} # used to hold trace.json
frame_number = 0 # keep track of which frame we are on
file_name = "" # what is the file we are running
current_line = 0 # what line number we're on
stack_depth = 1 # current stack depth
current_func_name = "" 
line_executed = ""
all_variables = ""
def append_frame():
    global frame_number
    frame_json["frame " + str(frame_number)] = \
    {"currentLine" : current_line, "codeNextToRun" : line_executed, "fileName" : file_name, \
    "stack" : {"numStackFrames" : stack_depth, "topStackFrame" : \
    {"methodName" : current_func_name, "variables" : all_variables } } }
    frame_number += 1
def print_frame_json():
    for frame in frame_json.keys():
        pprint(frame_json[frame])

# Start gdb process
gdbmi = GdbController()
# Load binary ex_prog1
gdbmi.write(f'-file-exec-file {sys.argv[1]}')
# load symbols from the executable
gdbmi.write(f'file {sys.argv[1]}')
# start running the program
response = gdbmi.write('start')
#print(response[2]['payload']['bkpt'])
current_func_name = response[2]['payload']['bkpt']['func']
file_name = response[2]['payload']['bkpt']['file']
current_line = response[2]['payload']['bkpt']['line']
strip_index = response[16]['payload'].strip("\\n").find("\\t")
line_executed = response[16]['payload'][strip_index + 2:].lstrip()
append_frame()
variable_updated = [line_executed.split(" ")[1]]
response = gdbmi.write('info locals') # get info about local vars
all_main_locals = ""
for i in range(1, len(response) - 1):
    all_main_locals += (response[i]['payload'].replace("\\n", ",") + " ")
all_variables = all_main_locals
while True:
    response = gdbmi.write('step') # send GDB to execute one line
    if ("__libc_start_main" in response[3]['payload']): # this checks for when we reach the end
        gdbmi.exit()
        break
    raw_info = ""
    #print(response)
    for object in response:
        if object['type'] == 'console':
            raw_info = object['payload'].strip("\\n")
            strip_index = raw_info.find("\\t")
            if (strip_index == -1):
                continue
            if "}" in raw_info and "{" not in raw_info:
                current_line = raw_info[:strip_index]
                line_executed = "return from " + current_func_name
                continue
            current_line = raw_info[:strip_index].rstrip() 
            line_executed = raw_info[strip_index + 2:].lstrip()

    raw_stack = gdbmi.write('bt')
    current_func_name = raw_stack[1]['payload'].split(" ")[2] + "()"
    stack_depth = len(raw_stack) - 2

    response = gdbmi.write('info locals') # get info about local vars
    #print(response)
    var_output = ""
    for i in range(1, len(response) - 1):
        var_output += (response[i]['payload'].strip("\\n") + " ")
    all_variables = var_output
    #print(var_output)
    append_frame()
    print(f"Executed line {current_line}")

out_file = open("trace.json", "w")
json.dump(frame_json, out_file, indent = 6)
out_file.close()
'''
strip_index = raw_info.find("\\t")
if (strip_index == -1):
    if file_name in raw_info:
        print("EXECUTING FUNCTION")
        raw_payload = gdbmi.write('bt')[1]['payload']
        current_func_name = raw_payload.split(" ")[2] + "()"
        stack_depth += 1
        raw_info = response[4]['payload'].strip("\\n")
        strip_index = raw_info.find("\\t")
        current_line = raw_info[:strip_index]
        line_executed = raw_info[strip_index + 2:].lstrip()
    else:
        print("WE GOT STDOUT")
else:
    if ("}" in raw_info) and ("{" not in raw_info):
        print("WE ARE RETURNING")
        stack_depth = stack_depth - 1
        current_line = raw_info[:strip_index]
        line_executed = "return from " + current_func_name
    else:
        print("EXECUTING LINE")
        current_line = raw_info[:strip_index]
        line_executed = raw_info[strip_index + 2:].lstrip()
'''