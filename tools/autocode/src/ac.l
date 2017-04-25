%option noyywrap nodefault yylineno
%{
#include "ac.tab.h"
%}
%%
"+" { return PLUS; }
"-" { return MINUS; }
"*" { return TIMES; }
"/" { return OVER; }
"(" { return OPEN_PARENTHESES; }
")" { return CLOSE_PARENTHESES; }
[0-9]+ { yylval = atoi(yytext); return VALUE; }
[a-zA-Z_][a-zA-Z0-9_]* { printf("IDENTITFIER %s\n", yytext); }
"//".*
\n { return NEWLINE; }
[ ] { /* ignore whitespace */ }
. { printf("Mystery character %c\n", *yytext); }
%%
/*
"#" { return ASSEMBLY_SYMBOL; }
*/
