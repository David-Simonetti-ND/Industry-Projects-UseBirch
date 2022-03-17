/* Infix notation calculator--calc */

%{
#define YYSTYPE int
#define YYERROR_VERBOSE
#define YYDEBUG 1
#include "globals.h"
%}

/* BISON Declarations */
%error-verbose
%verbose
%token NUM
%right ','
%right '}'

/* Grammar follows */
%%
input:  line 
;

line:       'N' { BPRINT2("%s", $1) } vector line
          | 'N' { BPRINT2("%s", $1) } deque line
          | 
;

deque:    'D' '[' { BPRINT("[") } vect_contents ']' { BPRINT("]") }
;

vector:   'V' '[' { BPRINT("[") } vect_contents ']' { BPRINT("]") }
;

vect_contents: var 
            | 'F' char
            | vector 
            | vect_contents ',' { BPRINT(",") }  vect_contents 

;

var:   int
     | string
;

int:  'F' { BPRINT2("%d", $1) };
string: 'S' { BPRINT2("%s", $1) };
char: 'C' { BPRINT2("%c", $1) };

%%
/* Lexical analyzer returns a double floating point 
   number on the stack and the token NUM, or the ASCII
   character read if not a number.  Skips all blanks
   and tabs, returns 0 for EOF. */

#include <ctype.h>

#include <stdio.h>

yyerror (char *s)  /* Called by yyparse on error */
{
  printf ("Error on line %d: %s\n", lineno, s);
}

main ()
{
  yyparse ();
}