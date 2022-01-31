#import "/escnfs/home/dsimone2/pygdbmi/build/lib/pygdbmi/gdbmiparser.py"
import sys

sys.path.insert(0, '/escnfs/home/dsimone2/pygdbmi/build/lib/')
from pygdbmi.gdbcontroller import GdbController
from pprint import pprint
import time

# Start gdb process
gdbmi = GdbController()
# Load binary ex_prog1
gdbmi.write('-file-exec-file ex_prog1')
# load symbols from the executable
gdbmi.write('file ex_prog1')
# start running the program
gdbmi.write('start')
while True:
    response = gdbmi.write('next') # send GDB to execute one line
    if ("__libc_start_main" in response[3]['payload']): # this checks for when we reach the end
        gdbmi.exit()
        break
    print("Code ran is: ", response[3]['payload'].rstrip()) # print out the line of code that was just ran
    response = gdbmi.write('info locals') # get info about local vars
    var_output = ""
    for i in range(1, len(response) - 1):
        var_output += (response[i]['payload'])
    print(var_output.rstrip())