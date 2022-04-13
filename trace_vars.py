import re, subprocess

punctMap = { # Only the braces in this map are used as of now. This is here so that if gdb returns a similar syntax for vectors or maps, adding them to the variable dictionary is easier
    '{': '}',
    '[': ']',
    '(': ')',
}

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

def define_val_type(val, name=None): # recursive function used to change strings into typed variables
    val = val.replace("\\n", "").replace("\\", "").rstrip("\"").lstrip("\"")
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
    if "std::" in val:
        parse_in = open('myinput.in', 'w')
        parse_in.write(f"{name} = {val}\n")
        parse_in.close()
        parse_in = open('myinput.in', 'r')
        #p = subprocess.Popen('parsing/parse', stdin=parse_in)
        #p.wait()
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