%{
#define YYERROR_VERBOSE
#define YYDEBUG 1
#include "globals.h"
%}

/* BISON Declarations */
%error-verbose
%verbose
%union
{
  int ival;
  double fval;
}
%token <ival> BNAME 400
%token <ival> BVECTOR 401
%token <ival> BDEQUE 402
%token <ival> BMAP 403
%token <ival> BARRAY 404

%token <ival> BINTEGER 300
%token <ival> BSTRING 301
%token <ival> BCHAR 302
%token <ival> BSSCOPE 303
%token <ival> BESCOPE 304
%token <ival> BSKEY 305
%token <ival> BNKEY 306
%token <ival> BCKEY 307
%token <fval> BFLOAT 308

%right ',' // important -- do not remove

/* Grammar follows */
%%
input:  line 
;

line:       BNAME { BPRINT2("%s", $1) } vector line
          | BNAME { BPRINT2("%s", $1) } deque line
          | BNAME { BPRINT2("%s", $1) } map line
          | BNAME { BPRINT2("%s", $1) } array line
          |
;

deque:    BDEQUE BSSCOPE { BPRINT("[") } vect_contents BESCOPE { BPRINT("]") }
;

vector:   BVECTOR BSSCOPE { BPRINT("[") } vect_contents BESCOPE { BPRINT("]") }
;

map:      BMAP BSSCOPE { BPRINT("{") } map_contents BESCOPE { BPRINT("}") }
;
array:    BSSCOPE BARRAY BSSCOPE { BPRINT("[") } vect_contents BESCOPE { BPRINT("]") } BESCOPE
;

key:      BSKEY { char *s = $1; s[strlen(s) - 4] = ' '; BPRINT2(" { %s", $1 + 1) }
        | BNKEY { BPRINT2(" { %d = ", $1) }
        | BCKEY { char *s = $1; s[strlen(s) - 4] = ' '; BPRINT2(" { %s", $1 + 1) }

map_contents:  key vector { BPRINT("} ") }
             | key var { BPRINT("} ") }
             | key BINTEGER char { BPRINT("} ") }
             | map_contents ',' { BPRINT(",") }  map_contents 

;

vect_contents: var 
             | BINTEGER char
             | vector 
             | vect_contents ',' { BPRINT(",") }  vect_contents 
;

var:   int
     | string
     | float
;

int:  BINTEGER { BPRINT2("%d", $1) };
string: BSTRING { BPRINT2("%s", $1) };
char: BCHAR { BPRINT2("%c", $1) };
float: BFLOAT { BPRINT2("%lf", $1) };

%%

yyerror (char *s)  /* Called by yyparse on error */
{
  printf ("Error on line %d, character number %d: %s\n", lineno, num_chars, s);
}

main ()
{
  yyparse ();
}