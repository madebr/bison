/*
  Copyright (C) 2008-2015, 2018-2020 Free Software Foundation, Inc.

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

%require "3.6"
// %debug
%define parse.trace

// parse.error: verbose custom detailed
//%define parse.error verbose
%define parse.error custom

%define api.push-pull both
//%define parse.error detailed
//%define parse.lac full

%language "python"
%locations
%verbose

%{
class Position:
  def __init__(self, row: int=1, col: int = 1):
    self.row = row
    self.col = col

  def __eq__(self, other: "Position") -> bool:
    return self.row == other.row and self.col == other.col

  def __lt__(self, other: "Position") -> bool:
    if self.row == other.row:
      return self.col < other.col
    return self.row < other.col

  def __str__(self) -> str:
    return "{}:{}".format(self.row, self.col)
%}


%code {
#FIXME: what defines does python backend provide?
# %define api.token.constructor
}

%%

result:
  list  { print($1) }
;

%nterm <list> list;

list:
  %empty     { Generates an empty list }
| list item  { $$ = $1; $$.append($2) }
;

%nterm <str> item;
%token <str> TEXT;
%token <int> NUMBER;

item:
  TEXT
| NUMBER  { $$ = str($1); }
;

%%

import sys

class SimpleLexer(YYParser.Lexer):
  def __init__(self):
    self.count = 0

  def yyerror(self, msg: str):
    print(msg, file=sys.stderr)

  def yylex(self) -> int:
    # Return the next token.
    stage, self.count = self.count, self.count + 1
    if stage == 0:
      return self.make_TEXT ("I have three numbers for you.")
    elif stage in (1, 2, 3):
      return self.make_NUMBER (stage)
    elif stage == 4:
      return self.make_TEXT ("And that's all!")
    else:
      return self.make_YYEOF ()

if __name__ == "__main__":
  parser = parser (SimpleLexer())
  result = parser.parse ()
  sys.exit(0 if result else 1)
