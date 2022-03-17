%{
#define YYERROR_VERBOSE
#define YYDEBUG 1
#include "globals.h"
%}

/* BISON Declarations */
%error-verbose
%verbose
%token BNAME 256
%token BVECTOR 257
%token BDEQUE 258
%token BINTEGER 259
%token BSTRING 260
%token BCHAR 261
%token BSSCOPE 262
%token BESCOPE 263
%right ',' // important -- do not remove

/* Grammar follows */
%%
input:  line 
;

line:       BNAME { BPRINT2("%s", $1) } vector line
          | BNAME { BPRINT2("%s", $1) } deque line
          | 
;

deque:    BDEQUE BSSCOPE { BPRINT("[") } vect_contents BESCOPE { BPRINT("]") }
;

vector:   BVECTOR BSSCOPE { BPRINT("[") } vect_contents BESCOPE { BPRINT("]") }
;

vect_contents: var 
             | 'F' char
             | vector 
             | vect_contents ',' { BPRINT(",") }  vect_contents 
;

var:   int
     | string
;

int:  BINTEGER { BPRINT2("%d", $1) };
string: BSTRING { BPRINT2("%s", $1) };
char: BCHAR { BPRINT2("%c", $1) };

%%

yyerror (char *s)  /* Called by yyparse on error */
{
  printf ("Error on line %d, character number %d: %s\n", lineno, num_chars, s);
}

main ()
{
  yyparse ();
}