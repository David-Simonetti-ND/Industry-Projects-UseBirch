/* Infix notation calculator--calc */

%{
#define YYSTYPE int
#define YYERROR_VERBOSE
#define YYDEBUG 1
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
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

line:     'N' {printf("%s", $1);} vector line
          | 
;

vector:   'V' '[' {printf("[");} vect_contents ']' {printf("]");}
;

vect_contents: var 
            | vector 
            | vect_contents ',' {printf(",");}  vect_contents 

;

var:   int
     | string
;

int:  'F' {printf("%d", $1);};
string: 'S' {printf("%s", $1);};

%%
/* Lexical analyzer returns a double floating point 
   number on the stack and the token NUM, or the ASCII
   character read if not a number.  Skips all blanks
   and tabs, returns 0 for EOF. */

#include <ctype.h>

#include <stdio.h>

yyerror (s)  /* Called by yyparse on error */
     char *s;
{
  printf ("Error: %s\n", s);
}

main ()
{
  yyparse ();
}