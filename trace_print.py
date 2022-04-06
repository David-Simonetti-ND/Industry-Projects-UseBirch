def print_frame_json(): # used to debug and print out all the frames currently in internal_trace_json
    pprint(internal_trace_json["frame " + str(current_frame_number - 1)])
punctMap = { # Only the braces in this map are used as of now. This is here so that if gdb returns a similar syntax for vectors or maps, adding them to the variable dictionary is easier
    '{': '}',
    '[': ']',
    '(': ')',
}