#!/usr/bin/env python
from pygdbmi.gdbcontroller import GdbController
from pprint import pprint
import time, sys, json, os, ast
import re

def check_vector(val):
    if "std::vector" in val:
    new_vector_string = ''
    closing_counter = 0
    test_case = True
    iter1 = 0
    test_break = 0
    
    if '{' not in val or '}' not in val:
        val = []
        return val

    while iter1 < len(val):
        test_break = 0
        if val[iter1] == '{':
            new_vector_string += '['
            iter2 = iter1 + 1
            while test_case:
                if val[iter2] == '{':
                    closing_counter += 1
                    val = val[iter2:]
                    iter1 = 0
                    test_break = -1
                    break
                elif val[iter2] == '}':
                    for i in range(iter1 + 1, iter2):
                        new_vector_string += val[i]
                    new_vector_string += ']'
                    val = val[iter2:]
                    iter1 = 0
                    test_break = -1
                    break
                iter2 += 1
        if test_break == 0:
            iter1 += 1
    
    for i in range(0, closing_counter):
        new_vector_string += ']'

    new_vector_string = [char for char in new_vector_string]

    for i in range(0, len(new_vector_string) - 1):
        if new_vector_string[i] == ']' and new_vector_string[i + 1] == '[':
            new_vector_string.insert(i + 1,',')
    
    new_vector_string = ''.join(new_vector_string)
        
    try:
        new_vector_string = ast.literal_eval(new_vector_string)
        return new_vector_string
    except:
        return []

s1 = "std::vector of length 0, capacity 0"
s2 = 