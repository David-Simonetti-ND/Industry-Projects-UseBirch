#!/usr/bin/env python
from pygdbmi.gdbcontroller import GdbController
from pprint import pprint
import time, sys, json, os, ast
import re
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
args = {}
command_line_args = []
def check_vector(val):
    new_vector_string = '' # this holds the string which will later be turned into a list and returned to the user. It is what usebirch wants to be displayed
    closing_counter = 0 # counts how many closing brackets we need depending on the dimension of the vector
    iter1 = 0 # iterator for while loop that goes through val
    test_break = 0 # checks if break has been called
    brackets_list = ['{', '}'] # list of brackets to check if the val contains any of them before proceeding
    
    if not all(x in val for x in brackets_list): # if we dont have any brackets, that means vector is empty so return empty list
        val = []
        return val

    while iter1 < len(val): # if it is not empty let's loop through the string val
        test_break = 0 # we have not breaked yet so set it = 0
        if val[iter1] == '{': # the val string uses brackets to tell us that the values/contents of the vector are about to follow
            new_vector_string += '[' # we actually need to use [ in the actual string though because we are returning a list and lists use []
            iter2 = iter1 + 1 #start iterating right after we found the first { and check for the contents of the vector
            while iter2 < len(val):
                if val[iter2] == '{': # if we found another { this means this vector is multidimensional 
                    closing_counter += 1 # multidimensional means we need more closing brackets
                    val = val[iter2:] # slice the string to start from where we found the second {
                    iter1 = 0 # we need to start going through the new string from the start of it so we set iter to 0 again
                    test_break = -1 # test break value is -1 so we now that we used break
                    break
                elif val[iter2] == '}': # if we found a }, that means that everything in between will be vector contents
                    for i in range(iter1 + 1, iter2): # for loop to store all the contents inside of the string new_vector_string
                        new_vector_string += val[i]
                    new_vector_string += ']' #close the string with one ]
                    val = val[iter2:] #slice the string to start from right after the closing
                    iter1 = 0 # we have to keep iterating through the rest of val but from where it starts
                    test_break = -1 # we are about to break so we have to set it to -1
                    break
                iter2 += 1 # iter2 used to go through the string after we find the first {
        if test_break == 0: # if this is 0 it means we haven't found a { yet so keep going by adding 1 to iter1
            iter1 += 1
    
    for i in range(0, closing_counter): # add all the ] if vector is multidimensional 
        new_vector_string += ']'

    new_vector_string = [char for char in new_vector_string] # make string a list to be able to work with it easily
    count_commas_between = 0
    for i in range(0, len(new_vector_string) - 1):
        if new_vector_string[i] == ']' and new_vector_string[i + 1] == '[': # add all the commas between the ][ if vector is MD
            new_vector_string.insert(i + 1,',')
            count_commas_between += 1
        if new_vector_string[i] == '"': # replace double quotes with single quotes for strings
            new_vector_string[i] = "'"
        if new_vector_string[i] == '\\': # remove all the unnecessary slashes
            new_vector_string[i] = ''

    # all the code below until the try: is called is for the case that it is a vector of chars
    count_chars = len(''.join(new_vector_string).split(',')) - count_commas_between # to see how many characters we are dealing with which are seperated by commas
    check_count_chars = 0 # counter to check whether we will actually find all the characters
    char_str = '' # string that will hold the answer
    for i in range(0, len(new_vector_string) - 2): # for loop to count the number of chracters we have
        if new_vector_string[i] == "'" and new_vector_string[i + 2] == "'":
            check_count_chars += 1
    if count_chars == check_count_chars: # check if we found all the characters 
        for i in range(0, len(new_vector_string)):
            if new_vector_string[i] == ',' and new_vector_string[i - 1]  == ']' and new_vector_string[i + 1] == '[':
                char_str += new_vector_string[i]
            if new_vector_string[i] == '[' or new_vector_string[i] == ']': # we need to add all the braces
                char_str += new_vector_string[i]
            if new_vector_string[i] == "'" and new_vector_string[i - 2] == "'" and new_vector_string[i + 1] != ']': # add the characters + the comma if we didn't reach the end
                char_str += "'" + new_vector_string[i - 1] + "'" + ','
            elif new_vector_string[i] == "'" and new_vector_string[i - 2] == "'" and new_vector_string[i + 1] == ']': # add character whithout comma if we reached end
                char_str += "'" + new_vector_string[i - 1] + "'" 
    
        new_vector_string = char_str # set the string we were working with equal to the temp string we made that holds the answer
            
    new_vector_string = ''.join(new_vector_string) # turn string back to a list

    try:
        new_vector_string = ast.literal_eval(new_vector_string) # turn string that looks like list to an actual list
        return new_vector_string
    except: # if not possible return empty list
        return []
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
def print_frame_json(): # used to debug and print out all the frames currently in internal_trace_json
    pprint(internal_trace_json["frame " + str(current_frame_number - 1)])
punctMap = { # Only the braces in this map are used as of now. This is here so that if gdb returns a similar syntax for vectors or maps, adding them to the variable dictionary is easier
    '{': '}',
    '[': ']',
    '(': ')',
}
def define_val_type(val): # recursive function used to change strings into typed variables
    val = val.strip("\\n").strip("\"").strip("\\")
    val = val.lstrip()
    if len(val) == 0:
        return val
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
    # process maps 
    if "std::map" in val:
        map = {}
        try: 
            val = val.split("{[",1)[1][0:-1]
        except:
            return val
        items = val.split(", [")
        for item in items:
            (key, value) = item.split("] = ", 1)
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

    # process vectors
    if "std::vector" in val:
        return check_vector(val)
      
    if re.match(r"(\d)+ '.'", val): #if the value matches a string that begins with any number of digits, then has a space and one character wrapped in single quotes
            val = val.split('\'')[1]

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
        val = define_val_type(val)
        try:
            if all_main_locals[key] != val:
                all_main_locals[key] = val
                local_variable_dictionary[key] = val
        except:
            continue
    append_frame() # create new stack frame
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