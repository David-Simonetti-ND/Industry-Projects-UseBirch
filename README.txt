General tasks for everyone:
Make an attempt to understand what is going on in trace.py. I tried my best to comment everything, but I am sure there will be questions and please feel free to ask me! If everyone is lost, we can find some time for everyone to get together and I can go over it.
Individual tasks:
Aidan: Currently, there is no entry in the trace.json for storing the arguments for the current function. Your goal is to add a "arguments" key to the dictionary which is the value of "topStackFrame". This would contain key value pairs for all the arguments of the current function. For example, if we were currently in main, it would look like this:
"frame 0": {
            "currentLine": "17",
            "codeNextToRun": "int x = factorial(5);",
            "fileName": "recursion.cpp",
            "stack": {
                  "numStackFrames": 1,
                  "topStackFrame": {
                        "methodName": "main()",
                        "variables": "x = 0 , ", 
                        "arguments": {"argc": 2, "argv": ["recurison", "someargument"]}   <-- 
                  }
            }
      },
Chris: The UseBirch website specifies that the trace.json output should have a stdout value. Everytime a line prints something to standard out, this key should contain the value of whatever is output to the standard out of the program. This example is taken off the trace website. If the line being ran was `std::cout << "Hello world!" << std::endl`, the output should be roughly similar to.
{
		"lineNumber": 2, 
		"filename": "main.cpp",
		"stdout": "Hello world!\n", <--
    "stack": {
      "numStackFrames": 2,
      "topStackFrame": {
	      "methodName": "add", 
        "variables": {
          "a": 5,
          "b": 5
        }
			}
    }
Kat: There exists a very confusing bug in the variables key/value pair currently. When we send the command "info locals" to GDB, it outputs every local variable, including the local variables that are uninitialized. For example, in the first line of the trace output for example.cpp, we get this
"frame 0": {
            "currentLine": "9",
            "codeNextToRun": "int a = 5;",
            "fileName": "example.cpp",
            "stack": {
                  "numStackFrames": 1,
                  "topStackFrame": {
                        "methodName": "main()",
                        "variables": "a = 0 , addFive = 32767 , myDouble = 2.0731389752015378e-317 , foo = {-9536 , 32767 , 0 , 0 , 4196576 } , "
                  }
            }
      },
Because a, addFive, myDouble, and foo are uninitialized we get garbage values currently assigned to them. For example, myDouble has yet to be initialized to 6, so whatever random value currently in the stack for myDouble corresponds to 2.0731389752015378e-317 which would be extremely confusing for a new programmer. Your task is twofold. First, as of right now the value of the variables key is simply one string. I would ask you turn this into a dictionary.
For example, turn  "variables": "a = 0 , addFive = 32767 , myDouble = 2.0731389752015378e-317 , foo = {-9536 , 32767 , 0 , 0 , 4196576 } , " into "variables": {"a": 0, "addFive":32767, "myDouble":2.0731389752015378e-317, "foo": [-9536 , 32767 , 0 , 0 , 4196576]}
After doing this, I would ask that you figure out some way to only display variables if they have been initialized. For example, take example.cpp. On the first line of the program we would not print any variable out because no variables have been set, but on the second line we run, a has been set, so it is safe to be able to output the value of a.
David: Work with situations where the program requires either command line arguments or input from stdin. Right now, the program only works if the executable takes in neither.