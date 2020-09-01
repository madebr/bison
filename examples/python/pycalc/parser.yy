%skeleton "lalr1.py" // -*- Python -*-
%require "3.6.4.103-9e750"
%defines

%define api.token.raw

%define api.token.constructor
%define api.value.type variant
%define parse.assert

 /**/
%code requires {
  from .driver import driver
}
 /**/

// The parsing context.
%param { drv: Driver }

%locations

%define parse.trace
%define parse.error detailed
%define parse.lac full

 /**/

%define api.token.prefix {TOK_}
%token
  ASSIGN  ":="
  MINUS   "-"
  PLUS    "+"
  STAR    "*"
  SLASH   "/"
  LPAREN  "("
  RPAREN  ")"
;

%token <str> IDENTIFIER "identifier"
%token <int> NUMBER "number"
%nterm <int> exp

%printer { print($$, file=yy) } <*>;

%%
%start unit;
unit: assignments exp  { drv.result = $2 };

assignments:
  %empty                 {}
| assignments assignment {};

assignment:
  "identifier" ":=" exp { drv.variables[$1] = $3 };

%left "+" "-";
%left "*" "/";
exp:
  "number"
| "identifier"  { $$ = drv.variables[$1] }
| exp "+" exp   { $$ = $1 + $3 }
| exp "-" exp   { $$ = $1 - $3 }
| exp "*" exp   { $$ = $1 * $3 }
| exp "/" exp   { $$ = $1 // $3 }
| "(" exp ")"   { $$ = $2 }
%%

def error(l: Location, m: str) -> None:
  print("{}: {}".format(l, m), file=sys.stderr)
