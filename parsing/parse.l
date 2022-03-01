%{
#include <stdio.h>
union yylval
{
    char *str;
    int num;
} yylval;
%}
%option noyywrap

SIGN (-?)
EQUALS (" =")
VECTOR ("std::vector of length ")
DEQUE ("std::deque with ")
ELEMENTS (" elements")
CAPACITY (", capacity ")
NUMBER [0-9]
CHAR [a-zA-Z]

%%


[a-zA-Z0-9]+{EQUALS} {yylval.str = strdup(yytext); return 'N';}
{VECTOR}{SIGN}{NUMBER}+{CAPACITY}{SIGN}{NUMBER}+{EQUALS} { return 'V'; }
\{ { return '[';}
\} { return ']';}
\n {printf("\n");}
{SIGN}[0-9]+ {yylval.num = atoi(yytext); return 'F'; }
\"{CHAR}+\" {yylval.str = strdup(yytext); return 'S'; }
, {return ',';}
{DEQUE}{SIGN}{NUMBER}+{ELEMENTS} { return 'D'; printf("D"); }
"std::queue wrapping: "
.
%%
//int main()
//{
//    yylex();
//}