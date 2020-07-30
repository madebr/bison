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
//%debug
%define parse.trace

// parse.error: verbose custom detailed
%define parse.error verbose
//%define parse.error custom

//%define api.push-pull both
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

%nterm <list> result;

result:
  list  {
  $$=$1 }
;

%nterm <list> list;

list:
  %empty     { $$ = [] }
| list item  {
  $$ = $1
  $$.append($2)
};

%nterm <str> item;
%token <str> TEXT;
%token <int> NUMBER;

item:
  TEXT
| NUMBER  {
    my_numbers = [1, 2, 3]
    if $1 in my_numbers:
      print("I know this number!")
    print("Received {}".format($1))
    print("{} ** 2 -> {}".format($1, $1*$1))
    $$ = str($1)
  }
;

%%

import sys

class SimpleLexer(YYParser.Lexer):
  def __init__(self):
    self.count = 0

  def yyerror(self, msg: str, *args) -> None:
    print(msg, file=sys.stderr)

  def yylex(self) -> Tuple[int, object]:
    # Return the next token.
    stage, self.count = self.count, self.count + 1
    if stage == 0:
      return self.TEXT, "I have four numbers for you."
    elif stage in (1, 2, 3, 4):
      return self.NUMBER, stage
    elif stage == 5:
      return self.TEXT, "And that's all!"
    else:
      return self.YYEOF, None

  def start_pos(self) -> Position:
    return Position()

  def end_pos(self) -> Position:
    return Position()


if __name__ == "__main__":
  lexer = SimpleLexer()
  parser = YYParser(lexer)
  result = parser.parse ()
  print("FINAL RESULT IS", result)
  sys.exit(0 if result else 1)
