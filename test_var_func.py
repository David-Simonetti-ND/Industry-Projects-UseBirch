#!/usr/bin/env python
from pygdbmi.gdbcontroller import GdbController
from pprint import pprint
import time, sys, json, os, ast
import re

def check_vector(val):
    if "std::vector" in val:
        new_vector_string = ''
        closing_counter = 0
        iter1 = 0
        test_break = 0
        brackets_list = ['{', '}']
        
        if not all(x in val for x in brackets_list):
            val = []
            return val

        while iter1 < len(val):
            test_break = 0
            if val[iter1] == '{':
                new_vector_string += '['
                iter2 = iter1 + 1
                while iter2 < len(val):
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
s2 = "std::vector of length 4, capacity 4 = {'a', 'b', 'c', 'd'}"
s3 = "std::vector of length 3, capacity 3 = {std::vector of length 3, capacity 3 = {1, 2, 3}, std::vector of length 3, capacity 3 = {4, 5, 6}, std::vector of length 3, capacity 3 = {7, 8, 9}}"
s4 = "std::vector of length 178956558, capacity 173351935 = {<error reading variable vectorSquared (Cannot access memory at address 0x7fff00000003)>"
s5 = "std::vector of length 4, capacity 4 = {97 'a', 98 'b', 99 'c', 100 'd'}"
s6 = "std::vector of length 2, capacity 2 = {\\\"Hello\\\", \\\"Goodbye\\\"}"
s7 = "std::vector of length 1, capacity 1 = {std::vector of length 3, capacity 3 = {\\\"Hi\\\", \\\"Some\\\", \\\"DHSIJFDSBGBGUFGEWFB\\\"}}"
s8 = "std::vector of length 2, capacity 2 = {'Hello', 'Goodbye'}"
s9 = "std::vector of length 2, capacity 2 = {3, 5}"
s10 = "std::vector of length 2, capacity 2 = {\\\"\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\020 VUUU\\\\000\\\\000\\\\034AWUUU\\\\000\\\\000\\\\060AWUUU\\\\000\\\\000<AWUUU\\\\000\\\\000<AWUUU\\\\000\\\\000PAWUUU\\\\000\\\\000TAWUUU\\\\000\\\\000TAWUUU\\\\000\\\\000!\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\260>WUUU\\\\000\\\\000\\\\020 VUUU\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000!\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\020AWUUU\\\\000\\\\000\\\\020 VUUU\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000!\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\060AWUUU\\\\000\\\\000\\\\020 VUUU\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\000\\\\241\\\\356\\\", '\\\\000' <repeats 30 times>..., \\\"Goodbye\\\"}"
s11 = "std::vector of length 1, capacity 1 = {std::vector of length 2932031011331, capacity 2932031011331 = {<error reading variable v1 (Cannot access memory at address 0x0)>"
print(check_vector(s8))
