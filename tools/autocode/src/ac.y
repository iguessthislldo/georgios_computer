%{
#include <stdio.h>

int yylex();
int yyerror(char *s) {
    fprintf(stderr, "error: %s\n", s);
}
%}

%token VALUE
%token PLUS MINUS TIMES OVER
%token NEWLINE
%token OPEN_PARENTHESES CLOSE_PARENTHESES
%token IDENTIFIER

%%

statement:
    | statement expression NEWLINE { printf("    =\n"); }
    ;

expression: factor
    | expression PLUS factor { printf("    +\n"); }
    | expression MINUS factor { printf("     -\n"); }
    ;

factor: term
    | factor TIMES term { printf("    *\n"); }
    | factor OVER term { printf("    /\n"); }
    ;

term:
    | VALUE { printf("    %d\n", $1); }
    | OPEN_PARENTHESES expression CLOSE_PARENTHESES { printf("    (%s)\n", $2); }
    ;
%%
int main(int argc, char **argv) {
    yyparse();
}

