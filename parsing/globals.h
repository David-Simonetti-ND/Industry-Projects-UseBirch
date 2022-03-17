#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <ctype.h>

enum TOKENS {NAME = 256, VECTOR, DEQUE, INTEGER, STRING, CHAR, SSCOPE, ESCOPE};
/*
#define VECTOR 'V'
#define DEQUE 'D'
#define INTEGER 'F'
#define STRING 'S'
#define CHAR 'C'
#define SSCOPE '['
#define ESCOPE ']'
*/

#define ENABLE_FLEX_OUTPUT 0
#define ENABLE_BISON_OUTPUT 1

#define FPRINT(string) if (ENABLE_FLEX_OUTPUT) {printf(string);}
#define FPRINT2(string, arg) if (ENABLE_FLEX_OUTPUT) {printf(string, arg);}

#define BPRINT(string) if (ENABLE_BISON_OUTPUT) {printf(string);}
#define BPRINT2(string, arg) if (ENABLE_BISON_OUTPUT) {printf(string, arg);}

int lineno;
