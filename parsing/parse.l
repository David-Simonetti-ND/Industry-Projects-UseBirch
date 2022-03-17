%{
#include "globals.h"
union yylval
{
    char *str;
    int num;
} yylval;
%}
%option noyywrap

SIGNEDNUM (-?)[0-9]+
CHAR [a-zA-Z]
CCHAR \'{CHAR}\'
STRING \"{CHAR}+\"
VECTOR "std::vector of length "{SIGNEDNUM}", capacity "{SIGNEDNUM}" ="
DEQUE "std::deque with "{SIGNEDNUM}" elements"
QUEUE "std::queue wrapping: "

%%


[a-zA-Z0-9]+" =" {   
                        yylval.str = strdup(yytext); 
                        FPRINT2("Tokenizing name: %s ", yylval.str) 
                        return NAME;
                    }
{VECTOR}            { 
                        FPRINT("Encountering vector\n");
                        return VECTOR; 
                    }
\{ { FPRINT("Starting scope [ "); return SSCOPE;}
\} { FPRINT("] Ending scope "); return ESCOPE;}
\n { printf("\n"); lineno++; }
{SIGNEDNUM} {
                        yylval.num = atoi(yytext); 
                        FPRINT2("Signed integer found: %d ", yylval.num) 
                        return INTEGER; 
             }
{STRING} {
                        yylval.str = strdup(yytext); 
                        FPRINT2("String found: %s ", yylval.str)
                        return STRING; 
            }
{CCHAR} {
        FPRINT("C CHAR")
        return CHAR;
        }
, { FPRINT(", ")  return ',';}
{DEQUE}     { 
            FPRINT("Encountering deque ")
            return DEQUE; 
            }
{QUEUE} {FPRINT("Encountering queue ")}

.
%%
//int main()
//{
//    yylex();
//}