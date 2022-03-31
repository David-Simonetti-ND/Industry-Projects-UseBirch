%{
#include "globals.h"
union yylval
{
    char *str;
    int num;
    double dbl;
} yylval;
int lineno = 0;
int num_chars = 0;
%}
%option noyywrap

SIGNEDNUM (-?)[0-9]+
FLOAT (-?)[0-9]+\.[0-9]+
CHAR [a-zA-Z]
CCHAR \'{CHAR}\'
STRING \"{CHAR}+\"
SKEY \[{STRING}\]" = "
NKEY \[{SIGNEDNUM}\]" = "
CKEY \[{SIGNEDNUM}" "{CCHAR}\]" = "

VECTOR "std::vector of length "{SIGNEDNUM}", capacity "{SIGNEDNUM}" ="
DEQUE "std::deque with "{SIGNEDNUM}" elements"
QUEUE "std::queue wrapping: "
STACK "std::stack wrapping: "
ARRAY "_M_elems = "

MAP "std::map with "{SIGNEDNUM}" elements ="
SET "std::set with "{SIGNEDNUM}" elements ="
MSET "std::multiset with "{SIGNEDNUM}" elements = "
USET "std::unordered_set with "{SIGNEDNUM}" elements"
UMSET "std::unordered_multiset with "{SIGNEDNUM}" elements"
DLLIST "std::list = "
SLLIST "std::forward_list = "


NAME [a-zA-Z0-9]+" ="

%%


{NAME}   {   
            yylval.str = strdup(yytext); 
            num_chars += strlen(yytext);
            FPRINT2("Tokenizing name: %s ", yylval.str) 
            return NAME;
         }
{VECTOR} { 
            num_chars += strlen(yytext);
            FPRINT("Encountering vector\n")
            return VECTOR; 
         }
{DEQUE}  { 
            num_chars += strlen(yytext);
            FPRINT("Encountering deque ")
            return DEQUE; 
         }
{QUEUE} {FPRINT("Encountering queue ") num_chars += strlen(yytext);}
{STACK} {FPRINT("Encountering stack ") num_chars += strlen(yytext);}
{MAP}   { 
            num_chars += strlen(yytext);
            FPRINT("Encountering map ")
            return MAP; 
         }
{SET}   { 
            num_chars += strlen(yytext);
            FPRINT("Encountering set ")
            return MAP; 
         }
{MSET}   { 
            num_chars += strlen(yytext);
            FPRINT("Encountering multiset ")
            return MAP; 
         }
{USET}   { 
            num_chars += strlen(yytext);
            FPRINT("Encountering unordered set ")
            return MAP; 
         }
{UMSET}   { 
            num_chars += strlen(yytext);
            FPRINT("Encountering unordered multiset ")
            return MAP; 
         }
{ARRAY} { 
            num_chars += strlen(yytext);
            FPRINT("Encountering array ")
            return ARRAY; 
         }
{DLLIST}   { 
            num_chars += strlen(yytext);
            FPRINT("Encountering doubly linked list ")
            return MAP; 
         }
{SLLIST}   { 
            num_chars += strlen(yytext);
            FPRINT("Encountering singley linked list ")
            return MAP; 
         }
\{ { FPRINT("Starting scope [ "); num_chars += strlen(yytext); return SSCOPE;}
\} { FPRINT("] Ending scope "); num_chars += strlen(yytext); return ESCOPE;}

\n { printf("\n"); lineno++; num_chars = 0; }
{FLOAT}    {
                yylval.dbl = atof(yytext); 
                num_chars += strlen(yytext);
                FPRINT2("Float found: %lf ", yylval.dbl) 
                return FLOAT; 
            }
{SIGNEDNUM} {
                yylval.num = atoi(yytext); 
                num_chars += strlen(yytext);
                FPRINT2("Signed integer found: %d ", yylval.num) 
                return INTEGER; 
            }
{STRING} {
            yylval.str = strdup(yytext); 
            num_chars += strlen(yytext);
            FPRINT2("String found: %s ", yylval.str)
            return STRING; 
         }
{SKEY}   {
            yylval.str = strdup(yytext); 
            num_chars += strlen(yytext);
            FPRINT2("String key found: %s ", yylval.str)
            return SKEY; 
         }
{NKEY}   {
            yylval.num = atoi(yytext + 1); 
            num_chars += strlen(yytext);
            FPRINT2("Integer key found: %d ", yylval.num) 
            return NKEY; 
         }
{CKEY}   {
            yylval.str = strdup(yytext + 3); 
            num_chars += strlen(yytext);
            FPRINT2("Char key found: %s ", yylval.str)
            return CKEY; 
         }
{CCHAR} {
        num_chars += strlen(yytext);
        FPRINT("C CHAR")
        return CHAR;
        }
, { FPRINT(", ") num_chars += strlen(yytext); return ',';}
.
%%