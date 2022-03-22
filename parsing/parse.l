%{
#include "globals.h"
union yylval
{
    char *str;
    int num;
} yylval;
int lineno = 0;
int num_chars = 0;
%}
%option noyywrap

SIGNEDNUM (-?)[0-9]+
CHAR [a-zA-Z]
CCHAR \'{CHAR}\'
STRING \"{CHAR}+\"
SKEY \[{STRING}\]" = "
NKEY \[{SIGNEDNUM}\]" = "
VECTOR "std::vector of length "{SIGNEDNUM}", capacity "{SIGNEDNUM}" ="
DEQUE "std::deque with "{SIGNEDNUM}" elements"
QUEUE "std::queue wrapping: "
MAP "std::map with "{SIGNEDNUM}" elements ="
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
{MAP}   { 
            num_chars += strlen(yytext);
            FPRINT("Encountering map ")
            return MAP; 
         }
\{ { FPRINT("Starting scope [ "); num_chars += strlen(yytext); return SSCOPE;}
\} { FPRINT("] Ending scope "); num_chars += strlen(yytext); return ESCOPE;}

\n { printf("\n"); lineno++; num_chars = 0; }
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
            FPRINT2("String found: %s ", yylval.str)
            return SKEY; 
         }
{NKEY}   {
            yylval.num = atoi(yytext + 1); 
            num_chars += strlen(yytext);
            FPRINT2("Integer key found: %d ", yylval.num) 
            return NKEY; 
         }
{CCHAR} {
        num_chars += strlen(yytext);
        FPRINT("C CHAR")
        return CHAR;
        }
, { FPRINT(", ") num_chars += strlen(yytext); return ',';}
.
%%