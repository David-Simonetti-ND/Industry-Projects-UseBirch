#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

enum PRIMITIVE_TOKENS {INTEGER = 300, STRING, CHAR, SSCOPE, ESCOPE, SKEY, NKEY, CKEY, FLOAT};
enum STRUCTURE_TOKENS {NAME = 400, VECTOR, DEQUE, MAP, ARRAY};


#define ENABLE_FLEX_OUTPUT 0
#define ENABLE_BISON_OUTPUT 1

#define FPRINT(string) if (ENABLE_FLEX_OUTPUT) {printf(string);}
#define FPRINT2(string, arg) if (ENABLE_FLEX_OUTPUT) {printf(string, arg);}

#define BPRINT(string) if (ENABLE_BISON_OUTPUT) {printf(string);}
#define BPRINT2(string, arg) if (ENABLE_BISON_OUTPUT) {printf(string, arg);}

extern int lineno;
extern int num_chars;