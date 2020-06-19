# Python skeleton for Bison                           -*- autoconf -*-

# Copyright (C) 2007-2015, 2018-2020 Free Software Foundation, Inc.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

m4_include(b4_skeletonsdir/[python.m4])

b4_defines_if([b4_complain([%defines does not make sense in Python])])

m4_define([b4_symbol_no_destructor_assert],
[b4_symbol_if([$1], [has_destructor],
              [b4_complain_at(m4_unquote(b4_symbol([$1], [destructor_loc])),
                              [%destructor does not make sense in Python])])])
b4_symbol_foreach([b4_symbol_no_destructor_assert])

# Setup some macros for api.push-pull.
b4_percent_define_default([[api.push-pull]], [[pull]])
b4_percent_define_check_values([[[[api.push-pull]],
                                 [[pull]], [[push]], [[both]]]])

# Define m4 conditional macros that encode the value
# of the api.push-pull flag.
b4_define_flag_if([pull]) m4_define([b4_pull_flag], [[1]])
b4_define_flag_if([push]) m4_define([b4_push_flag], [[1]])
m4_case(b4_percent_define_get([[api.push-pull]]),
        [pull], [m4_define([b4_push_flag], [[0]])],
        [push], [m4_define([b4_pull_flag], [[0]])])

# Define a macro to be true when api.push-pull has the value "both".
m4_define([b4_both_if],[b4_push_if([b4_pull_if([$1],[$2])],[$2])])

# Handle BISON_USE_PUSH_FOR_PULL for the test suite.  So that push parsing
# tests function as written, do not let BISON_USE_PUSH_FOR_PULL modify the
# behavior of Bison at all when push parsing is already requested.
b4_define_flag_if([use_push_for_pull])
b4_use_push_for_pull_if([
  b4_push_if([m4_define([b4_use_push_for_pull_flag], [[0]])],
             [m4_define([b4_push_flag], [[1]])])])

# Define a macro to encapsulate the parse state variables.  This
# allows them to be defined either in parse() when doing pull parsing,
# or as class instance variable when doing push parsing.
m4_define([b4_define_state],[[
  # Lookahead and lookahead in internal form.
  yychar = _YYEMPTY
  yytoken: ]b4_optional([SymbolKind])[ = None

  # State.
  yyn: int = 0
  yylen: int = 0
  yystate: int = 0
  yystack: _YYStack = _YYStack ()
  label: int = _YYNEWSTATE

]b4_locations_if([[
  # The location where the error started.
  yyerrloc: ]b4_optional(b4_location_type)[ = None

  # Location.
  yylloc: ]b4_location_type[ = ]b4_location_type[ (None, None)]])[

  # Semantic value of the lookahead.
  yylval: ]b4_optional(b4_yystype)[ = None
]])[

]b4_output_begin([b4_parser_file_name])[
]b4_copyright([Skeleton implementation for Bison LALR(1) parsers in Python],
              [2007-2015, 2018-2020])[
]b4_disclaimer[
]b4_percent_define_ifdef([package], [package b4_percent_define_get([package]);[
]])[
]b4_user_pre_prologue[
]b4_user_post_prologue[
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import List, IO, Optional, Tuple, Union
]b4_percent_code_get([[imports]])[
]b4_parser_class_declaration[
  """
     A Bison parser, automatically generated from <tt>]m4_bpatsubst(b4_file_name, [^"\(.*\)"$], [\1])[</tt>.
    
     :author: LALR (1) parser skeleton written by Paolo Bonzini.
  """
]b4_identification[
][
]b4_parse_error_bmatch(
           [detailed\|verbose], [[

  @@property
  def error_verbose(self) -> bool:
    """
     Whether verbose error messages are enabled.
    """
    return self._yy_error_verbose

  @@error_verbose.setter
  def error_verbose(self, verbose: bool) -> None:
    """
    Set the verbosity of error messages
    :param verbose True to request verbose error messages.
    """
    self._yy_error_verbose = verbose
]])[

]b4_locations_if([[
  class ]b4_location_type[:
    """
    A class defining a pair of positions.  Positions, defined by the
    <code>]b4_position_type[</code> class, denote a point in the input.
    Locations represent a part of the input through the beginning
    and ending positions.
    """
    __slots__ = ["begin", "end"]

    def __init__(self, begin: ]b4_optional(b4_position_type)[, end: ]b4_optional(b4_position_type)[=None):
      """
      Create a `Location` from the endpoints of the range.
      :param begin: The first, inclusive, position in the range.
      :param end: The first position beyond the range. If None, denote an empty range.
      """
      """ The first, inclusive, position in the range. """
      self.begin = begin or ]b4_position_type[ ()
      """ The first position beyond the range. """
      self.end = end or self.begin

    def __str__(self) -> str:
      if self.begin == self.end:
        return str(self.begin)
      else:
        return "{}-{}".format(self.begin, self.end)
]])[
  class _YYStack:
    __slots__ = ("_state_stack"]b4_locations_if([[, "_loc_stack"]])[, "_value_stack", "size", "height")
    def __init__(self):
      self._state_stack: ]b4_list([int])[ = [0] * 16 ] b4_locations_if([[
      self._loc_stack: ]b4_list(b4_optional(b4_location_type_full))[ = [None for _ in range(16)]]])[
      self._value_stack: ]b4_list(b4_optional(b4_yystype))[ = [None for _ in range(16)]

      self.size: int = 16
      self.height: int = -1

    def push(self, state: int, value: ]b4_yystype[]b4_locations_if([[, loc: ]b4_location_type_full])[) -> None:
      self.height += 1
      if self.size == self.height:
        self._state_stack += [0] * len(self._state_stack)]b4_locations_if([[
        self._loc_stack += [None] * len(self._loc_stack)]])[
        self._value_stack += [None] * len(self._value_stack)

        self.size *= 2

      self._state_stack[self.height] = state]b4_locations_if([[
      self._loc_stack[self.height] = loc]])[
      self._value_stack[self.height] = value

    def pop(self, num: int=1) -> None:
      if 0 < num:
        self._value_stack[self.height - num + 1:self.height + 1] = [None] * num]b4_locations_if([[
        self._loc_stack[self.height - num + 1:self.height + 1] = [None] * num]])[
      self.height -= num

    def state_at(self, idx: int) -> int:
      return self._state_stack[self.height - idx]
]b4_locations_if([[
    def location_at (self, idx: int) -> ]b4_location_type_full[:
      return self._loc_stack[self.height - idx]
]])[
    def value_at(self, idx: int) -> ]b4_yystype[:
      return self._value_stack[self.height - idx]

    def print_out(self, out: IO) -> None:
      """
      Print the state stack on the debug stream.
      """
      print("Stack now", file=out, end="")

      for i in range(self.height + 1):
        print(" ", file=out, end="")
        print(self._state_stack[i], file=out, end="")
      print(file=out)
]b4_locations_if([[
  @@classmethod
  def _yylloc(cls, rhs: _YYStack, n: int) -> ]b4_location_type[:
    if 0 < n:
      return cls.]b4_location_type[(rhs.location_at(n-1).begin, rhs.location_at(0).end)
    else:
      return cls.]b4_location_type[(rhs.location_at(0).end)
]])[
]b4_declare_symbol_enum[

  class Lexer(ABC):
    """
    Communication interface between the scanner and the Bison-generated
   parser <tt>]b4_parser_class[</tt>.
    """
]b4_token_enums[
    """ Deprecated, use ]b4_symbol(0, id)[ instead.  """
    EOF: int = ]b4_symbol(0, id)[
]b4_pull_if([b4_locations_if([[
    @@property
    @@abstractmethod
    def start_pos(self) -> ]b4_position_type[:
      """
      Method to retrieve the beginning position of the last scanned token.
      :return: the position at which the last scanned token starts.
      """
      pass

    @@property
    @@abstractmethod
    def end_pos(self) -> ]b4_position_type[:
      """
      Method to retrieve the beginning position of the last scanned token.
      :return: the position at which the last scanned token starts.
      """
      pass
]])[
    @@property
    @@abstractmethod
    def lval(self) -> ]b4_yystype[:
      """
      Method to retrieve the semantic value of the last scanned token.
      :return: the semantic value of the last scanned token.
      """
      pass

    @@abstractmethod
    def yylex(self) -> int:
      """
      Entry point for the scanner.  Returns the token identifier corresponding
      to the next token and prepares to return the semantic value
      ]b4_locations_if([and beginning/ending positions ])[of the token.
      :return: the token identifier corresponding to the next token.
      """
      pass
]])[
    @@abstractmethod
    def yyerror(]b4_locations_if([[loc: ]b4_optional("b4_location_type_full")[, ]])[msg: str) -> None:
      """
      Emit an error]b4_locations_if([ referring to the given location])[in a user-defined way.

      ]b4_locations_if([[ :param loc: The location of the element to which the
                      error message is related.]])[
      :param msg The string for the error message.
      """
      pass

]b4_parse_error_bmatch(
           [custom], [[
     @@abstractmethod
     def report_syntax_error (][ctx: "]b4_parser_class.[Context") -> None:
       """
         Build and emit a "syntax error" message in a user-defined way.
        :param ctx: The context of the error.
       """
       pass
]])[
]b4_lexer_if([[
  class _YYLexer(Lexer):
]b4_percent_code_get([[lexer]])])
b4_parse_param_vars[

]b4_lexer_if([[
  def __init__(self, ]b4_parse_param_decl([b4_lex_param_decl])[):
    """
      Instantiates the Bison-generated parser.
    """
]b4_percent_code_get([[init]])[
    """ The object doing lexical analysis for us. """
    self.yylexer: Lexer = YYLexer (]b4_lex_param_call[)
]b4_parse_param_cons[
]])[

  def __init__(self, ]b4_parse_param_decl([[lexer: Lexer]])[):
    """
      Instantiates the Bison-generated parser.
      :param yylexer The scanner that will supply tokens to the parser.
    """]
b4_percent_code_get([[init]])[
    """ The object doing lexical analysis for us. """
    self.yylexer: Lexer = lexer
]b4_parse_param_cons[
]b4_parse_error_bmatch(
           [detailed\|verbose], [[
    """ True if verbose error messages are enabled. """
    self._yy_error_verbose: bool = True
]])[
]b4_parse_trace_if([[
    """ The stream on which the debugging output is printed. """
    self._yy_debug_stream: IO = sys.stderr

    _yydebug: int = 0

    """ The number of syntax errors so far. """
    self._yynerrs: int = 0

    self._yyerrstatus: int = 0
]b4_push_if([[
    self._push_parse_initialized: bool = False
]])[

  @@property
  def debug_stream(self) -> IO:
    """
    :return: The stream on which the debugging output is printed. 
    """
    return self._yy_debug_stream

  @@debug_stream.setter
  def debug_stream(self, debug_stream: IO) -> None:
    """
    Set the stream on which the debug output is printed.
    :param debug_stream:  The stream that is used for debugging output.
    """
    self._yy_debug_stream = debug_stream

  @@property
  def debug_level(self) -> int:
    """
    Verbosity of the debugging output;
    0 means that all kinds of output from the parser are suppressed.
    :return: verbosity level
    """
    return self._yydebug

  @@debug_level.setter
  def debug_level(self, debug_level: int) -> None:
    """
    Set the verbosity of the debugging output;
    0 means that all kinds of output from the parser are suppressed.
    :param debug_level: The verbosity level for debugging output.
    """
    self._yydebug = debug_level
]])[
  @@property
  def number_errors(self) -> int:
    """
    :return: The number of syntax errors so far.
    """
    return self._yynerrs

  def yyerror(self, msg: str]b4_locations_if([[, posloc: ]b4_optional(b4_union(b4_location_type[, ]b4_position_type))[=None]])[) -> None:
    """
    Print an error message via the lexer.
    ]b4_locations_if([[Use a `None` location.]])[
    :param msg: The error message.
    :param posloc: A position object, a location object, or None.
    """
    if isinstance(posloc, Location):
      posloc = Position(posloc)
    self.yylexer.yyerror(]b4_locations_if([[posloc, ]])[msg)
]b4_parse_trace_if([[
  def _yycdebug (self, s: str) -> None:
    if 0 < self._yydebug:
      print(s, file=self._yy_debug_stream)
]])[
  """ Returned by a Bison action in order to stop the parsing process and 
    return success (True). """
  YYACCEPT: int = 0

  """ Returned by a Bison action in order to stop the parsing process and
   return failure (False). """
  YYABORT: int = 1

]b4_push_if([
  """ Returned by a Bison action in order to request a new token. """
  YYPUSH_MORE: int = 4])[

  """ Returned by a Bison action in order to start error recovery without
    printing an error message. """
  YYERROR: int = 2

  """
    Internal return codes that are not supported for user semantic actions.
  """
  _YYERRLAB: int = 3
  _YYNEWSTATE: int = 4
  _YYDEFAULT: int = 5
  _YYREDUCE: int = 6
  _YYERRLAB1: int = 7
  _YYRETURN: int = 8
]b4_push_if([[
  """ Signify that a new token is expected when doing push-parsing. """
  _YYGETTOKEN: int = 9 ]])[

]b4_push_if([b4_define_state])[
  def recovering(self) -> bool:
    """
    Whether error recovery is being done.  In this state, the parser
    reads token until it reaches a known state, and then restarts normal
    operation.
    """
    return self._yyerrstatus == 0

  def _yyLRGotoState(self, yystate: int, yysym: int) -> int:
    """
    Compute post-reduction state.
    :param yystate: the current state
    :param yysym:   the nonterminal to push on the stack
    """
    yyr = self._yypgoto[yysym - _YYNTOKENS] + yystate
    if 0 <= yyr <= _YYLAST and _yycheck[yyr] == yystate:
      return self._yytable[yyr]
    else:
      return self._yydefgoto[yysym - _YYNTOKENS]

  def _yyaction(self, yyn: int, yystack: _YYStack, yylen: int):
    """
    If YYLEN is nonzero, implement the default value of the action:
    '$$ = $1'.  Otherwise, use the top of the stack.

    Otherwise, the following line sets YYVAL to garbage.
    This behavior is undocumented and Bison
    users should not rely upon it.
    """
    yyval: ]b4_yystype[ = self._yystack.value_at(yylen - 1) if 0 < self.yylen else self._yystack.value_at(0)]b4_locations_if([[
    yyloc: ]b4_location_type[ = self._yylloc(yystack, yylen)]])[]b4_parse_trace_if([[

    self._yy_reduce_print(yyn, yystack)]])[

    while True:
      ]b4_user_actions[
      break
      ]b4_parse_trace_if([[

    self._yy_symbol_print("-> $$ =", SymbolKind(_yyr1[yyn]), yyval]b4_locations_if([, yyloc])[)]])[

    yystack.pop(yylen)
    yylen = 0
    # Shift the result of the reduction.
    yystate: int = self._yyLRGotoState(self._yystack.state_at(0), self._yyr1[yyn])
    yystack.push(yystate, yyval]b4_locations_if([, yyloc])[)
    return self._YYNEWSTATE

]b4_parse_trace_if([[

  def _yy_symbol_print(self, s: str, yykind: SymbolKind,
                       yyvalue: ]b4_yystype[]b4_locations_if([, yylocation: ]b4_location_type)[):
    """
    Print this symbol on YYOUTPUT.
    """
    if 0 < yydebug:
        self._yycdebug(s
                 + (yykind.value < YYNTOKENS_ ? " token " : " nterm ")
                 + yykind.name + " ("]b4_locations_if([
                 + yylocation + ": "])[
                 + (yyvalue == null ? "(null)" : yyvalue.toString()) + ")")
]])[

]b4_push_if([],[[
  def parse(self) -> int:
    """
    Parse input from the scanner that was specified at object construction
    time.  Return whether the end of the input was reached successfully.
    :return: <tt>true</tt> if the parsing succeeds.  Note that this does not
              imply that there were no syntax errors.
    """
  ]])[
]b4_push_if([[
  def push_parse(self, yylextoken: int, yylexval: ]b4_yystype[]b4_locations_if([, yylexloc: b4_location_type])[) -> int:
    """
    Push Parse input from external lexer
    
    :param yylextoken: current token
    :param yylexval: current lval]b4_locations_if([[
    :param yylexloc: current position]])[
    
    :return: <tt>YYACCEPT, YYABORT, YYPUSH_MORE</tt>
    """
  ]])[
   ]b4_locations_if([[
    # @@$.
    yyloc: ]b4_location_type_full[ = ]b4_location_type_full[()]])
b4_push_if([],[[
]b4_define_state[]b4_parse_trace_if([[
    self._yycdebug ("Starting parse")]])[
    self._yyerrstatus = 0
    self._yynerrs = 0

    # Initialize the stack.
    self._yystack.push (yystate, yylval]b4_locations_if([, yylloc])[)
]m4_ifdef([b4_initial_action], [
b4_dollar_pushdef([yylval], [], [], [yylloc])dnl
    b4_user_initial_action
b4_dollar_popdef[]dnl
])[
]])[
]b4_push_if([[
    if not self._push_parse_initialized:
      push_parse_initialize ()
]m4_ifdef([b4_initial_action], [
b4_dollar_pushdef([yylval], [], [], [yylloc])dnl
      b4_user_initial_action
b4_dollar_popdef[]dnl
])[]b4_parse_trace_if([[
      self._yycdebug ("Starting parse")]])[
      self._yyerrstatus = 0
    else:
      label = YYGETTOKEN

    push_token_consumed: bool = True
]])[
    for (;;)
      switch (label)
      {
        /* New state.  Unlike in the C/C++ skeletons, the state is already
           pushed when we come here.  */
      case _YYNEWSTATE:]b4_parse_trace_if([[
        self._yycdebug ("Entering state " + yystate)
        if (0 < yydebug)
          yystack.print_out (yyDebugStream)]])[

        /* Accept?  */
        if (yystate == YYFINAL_)
          ]b4_push_if([{label = YYACCEPT; break;}],
                      [return true;])[

        /* Take a decision.  First try without lookahead.  */
        self.yyn = _yypact[yystate]
        if (yyPactValueIsDefault (self.yyn))
          {
            label = _YYDEFAULT
            break
          }
]b4_push_if([        /* Fall Through */

      case YYGETTOKEN:])[
        /* Read a lookahead token.  */
        if (yychar == _YYEMPTY)
          {
]b4_push_if([[
            if (!push_token_consumed)
              return YYPUSH_MORE;]b4_parse_trace_if([[
            self._yycdebug ("Reading a token")]])[
            yychar = yylextoken
            yylval = yylexval]b4_locations_if([
            yylloc = yylexloc])[
            push_token_consumed = false]], [b4_parse_trace_if([[
            self._yycdebug ("Reading a token")]])[
            yychar = yylexer.yylex ()
            yylval = yylexer.getLVal()]b4_locations_if([[
            yylloc = ]b4_location_type[(yylexer.start_position,
                                        yylexer.end_position)]])[
]])[
          }

        /* Convert token to internal form.  */
        yytoken = yytranslate_ (yychar)]b4_parse_trace_if([[
        self._yy_symbol_print("Next token is", yytoken,
                              yylval]b4_locations_if([, yylloc])[)]])[

        if (yytoken == ]b4_symbol(1, kind)[)
          {
            // The scanner already issued an error message, process directly
            // to error recovery.  But do not keep the error token as
            // lookahead, it is too special and may lead us to an endless
            // loop in error recovery. */
            yychar = Lexer.]b4_symbol(2, id)[
            yytoken = ]b4_symbol(2, kind)[]b4_locations_if([[
            yyerrloc = yylloc]])[
            label = _YYERRLAB1
          }
        else:
          {
            # If the proper action on seeing token YYTOKEN is to reduce or to
            # detect an error, take that action.
            self.yyn += yytoken.value
            if self.yyn < 0 or self._YYLAST < self.yyn or yycheck_[self.yyn] != yytoken.value:
              label = _YYDEFAULT

            /* <= 0 means reduce or error.  */
            elif ((self.yyn = yytable[self.yyn]) <= 0)
              {
                if (yyTableValueIsError (self.yyn))
                  label = _YYERRLAB
                else
                  {
                    self.yyn = -self.yyn
                    label = _YYREDUCE
                  }
              }

            else
              {
                /* Shift the lookahead token.  */]b4_parse_trace_if([[
                self._yy_symbol_print("Shifting", yytoken,
                                      yylval]b4_locations_if([, yylloc])[)
]])[
                /* Discard the token being shifted.  */
                yychar = _YYEMPTY

                /* Count tokens shifted since error; after three, turn off error
                   status.  */
                if _yyerrstatus > 0:
                  _yyerrstatus -= 1

                yystate = self.yyn
                yystack.push (yystate, yylval]b4_locations_if([, yylloc])[)
                label = self._YYNEWSTATE
              }
          }
        break

      /*-----------------------------------------------------------.
      | yydefault -- do the default action for the current state.  |
      `-----------------------------------------------------------*/
      case _YYDEFAULT:
        self.yyn = _yydefact[yystate]
        if self.yyn == 0:
          label = _YYERRLAB
        else:
          label = _YYREDUCE
        break

      /*-----------------------------.
      | yyreduce -- Do a reduction.  |
      `-----------------------------*/
      case _YYREDUCE:
        self.yylen = _yyr2[self.yyn]
        label = yyaction(self.yyn, yystack, self.yylen)
        yystate = yystack.stateAt (0)
        break

      /*------------------------------------.
      | yyerrlab -- here on detecting error |
      `------------------------------------*/
      case _YYERRLAB:
        /* If not already recovering from an error, report this error.  */
        if self._yyerrstatus == 0:
          {
            ++self._yynerrs
            if (yychar == _YYEMPTY)
              yytoken = null
            yyreportSyntaxError (new Context (yystack, yytoken]b4_locations_if([[, yylloc]])[))
          }
]b4_locations_if([[
        yyerrloc = yylloc]])[
        if _yyerrstatus == 3:
          {
            /* If just tried and failed to reuse lookahead token after an
               error, discard it.  */

            if (yychar <= Lexer.]b4_symbol(0, id)[)
              {
                /* Return failure if at end of input.  */
                if (yychar == Lexer.]b4_symbol(0, id)[)
                  ]b4_push_if([{label = YYABORT; break;}], [return false;])[
              }
            else
              yychar = _YYEMPTY
          }

        /* Else will try to reuse lookahead token after shifting the error
           token.  */
        label = _YYERRLAB1
        break

      /*-------------------------------------------------.
      | errorlab -- error raised explicitly by YYERROR.  |
      `-------------------------------------------------*/
      case YYERROR:]b4_locations_if([[
        yyerrloc = yystack.locationAt (self.yylen - 1);]])[
        /* Do not reclaim the symbols of the rule which action triggered
           this YYERROR.  */
        yystack.pop (self.yylen)
        self.yylen = 0
        yystate = yystack.stateAt (0)
        label = _YYERRLAB1
        break

      /*-------------------------------------------------------------.
      | yyerrlab1 -- common code for both syntax error and YYERROR.  |
      `-------------------------------------------------------------*/
      case _YYERRLAB1:
        _yyerrstatus = 3       /* Each real token shifted decrements this.  */

        // Pop stack until we find a state that shifts the error token.
        for (;;)
          {
            self.yyn = _yypact[yystate]
            if (!yyPactValueIsDefault (self.yyn))
              {
                self.yyn += ]b4_symbol(1, kind)[.value
                if (0 <= self.yyn && self.yyn <= _YYLAST
                    && yycheck_[yyn] == ]b4_symbol(1, kind)[.value)
                  {
                    yyn = _yytable[self.yyn]
                    if 0 < yyn:
                      break
                  }
              }

            /* Pop the current state because it cannot handle the
             * error token.  */
            if (yystack.height == 0)
              ]b4_push_if([{label = YYABORT; break;}],[return false;])[

]b4_locations_if([[
            yyerrloc = yystack.locationAt (0);]])[
            yystack.pop ()
            yystate = yystack.stateAt (0);]b4_parse_trace_if([[
            if (0 < yydebug)
              yystack.print_out (yyDebugStream)]])[
          }

        if (label == YYABORT)
          /* Leave the switch.  */
          break

]b4_locations_if([[
        /* Muck with the stack to setup for yylloc.  */
        yystack.push (0, null, yylloc)
        yystack.push (0, null, yyerrloc
        yyloc = yylloc (yystack, 2)
        yystack.pop (2)]])[

        /* Shift the error token.  */]b4_parse_trace_if([[
        self._yy_symbol_print("Shifting", SymbolKind(yystos_[self.yyn]),
                              yylval]b4_locations_if([, yyloc])[)]])[

        yystate = self.yyn
        yystack.push (self.yyn, yylval]b4_locations_if([, yyloc])[)
        label = self._YYNEWSTATE
        break

        /* Accept.  */
      case YYACCEPT:
        ]b4_push_if([self._push_parse_initialized = false; return YYACCEPT;],
                    [return true;])[

        /* Abort.  */
      case YYABORT:
        ]b4_push_if([self._push_parse_initialized = false; return YYABORT;],
                    [return false;])[
      }
}
]b4_push_if([[

  def push_parse_initialize (self) -> None:
    """
    (Re-)Initialize the state of the push parser.
    """
    # Lookahead and lookahead in internal form.
    self.yychar = self._YYEMPTY
    self.yytoken = None

    """ State.  """
    self.yyn = 0
    self.yylen = 0
    self._yystate = 0
    self._yystack = _YYStack()
    self.label = self._YYNEWSTATE

    # Error handling.
    self._yynerrs = 0;]b4_locations_if([[
    # The location where the error started.
    self.yyerrloc = None
    self.yylloc = ]b4_location_type_full[ (None, None)]])[

    # Semantic value of the lookahead.
    self.yylval = None

    self._yystack.push (self._yystate, self.yylval]b4_locations_if([, self.yylloc])[)

    self._push_parse_initialized = True

]b4_locations_if([[
  def push_parse(self, yylextoken: int, yylexval: ]b4_yystype[, yylexpos: ]b4_position_type[) -> int:
    """
    Push parse given input from an external lexer.

    :param yylextoken: current token
    :param yylexval: current lval
    :param yyylexpos: current position

    :return: <tt>YYACCEPT, YYABORT, YYPUSH_MORE</tt>
    """
    return self.push_parse(yylextoken, ]b4_location_type[(yylexpos))
]])])[

]b4_both_if([[
  def parse(self) -> bool:
    """
    Parse input from the scanner that was specified at object construction
    time.  Return whether the end of the input was reached successfully.
    This version of parse() is defined only when api.push-push=both.

    :return: <tt>True</tt> if the parsing succeeds.  Note that this does not
             imply that there were no syntax errors.
    """
    if self.yylexer is None:
      raise ValueError("lexer is None")
    while True:
      token: int = self.yylexer.yylex()
      lval: ]b4_yystype[ = self.yylexer.getLVal()]b4_locations_if([[
      yyloc: ]b4_location_type[ = ]b4_location_type[(self.yylexer.start_position, self.yylexer.end_position)
      status = push_parse(token, lval, yyloc)]], [[
      status = push_parse(token, lval)]])[
      if status != self.YYPUSH_MORE:
        break
    return status == self.YYACCEPT
]])[

  class Context:
    """
    Information needed to get the list of expected tokens and to forge
    a syntax error diagnostic.
    """
    __slots__ = ("_yystack", "_yytoken"]b4_locations_if([[, "_yylocation"]])[)

    def __init__(self, stack: _YYStack, token: SymbolKind]b4_locations_if([, loc: ]b4_location_type)[):
      self._yystack: _YYStack = stack
      self._yytoken: ]b4_optional(SymbolKind)[ = token]b4_locations_if([[
      self._yylocation: ]b4_location_type[ = loc]])[

    @@property
    def token(self) -> ]b4_optional([SymbolKind])[:
      """ The symbol kind of the lookahead token. """
      return self._yytoken]b4_locations_if([[

    @@property
    def location(self) -> ]b4_location_type[:
      """ The location of the lookahead. """
      return self._yylocation]])[

    NTOKENS: int = ]b4_parser_class[._YYNTOKENS

    def get_expected_tokens(self, yyargn: List[int], int yyargn, yyoffset: int=0)-> int:
      """
      Put in YYARG at most YYARGN of the expected tokens given the
      current YYCTX, and return the number of tokens stored in YYARG.  If
      YYARG is null, return the number of expected tokens (guaranteed to
      be less than YYNTOKENS).
      """
      yycount: int = yyoffset
      yyn: int = ]b4_parser_class[._yypact[self._yystack.state_at (0)]
      if not yyPactValueIsDefault (yyn):
        """
        Start YYX at -YYN if negative to avoid negative
        indexes in YYCHECK.  In other words, skip the first
        -YYN actions for this state because they are default
        actions.
        """
        yyxbegin = -yyn if yyn < 0 else 0
        # Stay within bounds of both yycheck and yytname.
        yychecklim: int = _YYLAST - yyn + 1
        yyxend: int = yychecklim if yychecklim < self.NTOKENS else self.NTOKENS
        for yyx in range(yyxbegin, yyxend):
          if ]b4_parser_class[.yycheck_[yyx + yyn] == yyx and yyx != ]b4_symbol(1, kind)[.get_code()
              and not yyTableValueIsError(_yytable[yyx + yyn]):
            if yyarg is None:
              yycount += 1
            elif yycount == yyargn:
              return 0 # FIXME: this is incorrect.
            else:
              yyarg[yycount] = SymbolKind(yyx)
              yycount += 1
      if yyarg is not None and yycount == yyoffset && yyoffset < yyargn:
        yyarg[yycount] = None
      return yycount - yyoffset

]b4_parse_error_bmatch(
[detailed\|verbose], [[
  def _yysyntaxErrorArguments(self, yyctx: Context, yyarg: List[SymbolKind], yyargn: int) -> int:
    """
    There are many possibilities here to consider:
       - If this state is a consistent state with a default action,
         then the only way this function was invoked is if the
         default action is an error action.  In that case, don't
         check for expected tokens because there are none.
       - The only way there can be no lookahead present (in tok) is
         if this state is a consistent state with a default action.
         Thus, detecting the absence of a lookahead is sufficient to
         determine that there is no unexpected or expected token to
         report.  In that case, just report a simple "syntax error".
       - Don't assume there isn't a lookahead just because this
         state is a consistent state with a default action.  There
         might have been a previous inconsistent state, consistent
         state with a non-default action, or user semantic action
         that manipulated yychar.  (However, yychar is currently out
         of scope during semantic actions.)
       - Of course, the expected token list depends on states to
         have correct lookahead information, and it depends on the
         parser not to perform extra reductions after fetching a
         lookahead from the scanner and before detecting a syntax
         error.  Thus, state merging (from LALR or IELR) and default
         reductions corrupt the expected token list.  However, the
         list is correct for canonical LR with one exception: it
         will still contain any token that will not be accepted due
         to an error action in a later state.
    """
    yycount: int = 0
    if yyctx.token is not None:
      if yyarg is not None:
        yyarg[yycount] = yyctx.token
      yycount += 1
      yycount += yyctx.get_expected_tokens(yyarg, yyargn, 1)
    return yycount
]])[

  def _yyreport_syntax_error(self, yyctx: Context):
    """
    Build and emit a "syntax error" message in a user-defined way.
    :param ctx: The context of the error.
    """]b4_parse_error_bmatch(
[custom], [[
    self.yylexer.report_syntax_error(yyctx)]],
[detailed\|verbose], [[
    if self._yy_error_verbose:
      ARGMAX: int = 5
      yyarg: List[self.SymbolKind] = [None for _ in range(ARGMAX)]
      yycount: int = self.yysyntaxErrorArguments(yyctx, yyarg, ARGMAX)
      yystr: List[str] = [yyarg[yyi].name for yyi in range(yycount)]
      yyformat = None
      if yycount == 0:
        yyformat = ]b4_trans(["syntax error"])[
      elif yycount == 1:
        yyformat = ]b4_trans(["syntax error, unexpected {0}"])[
      elif yycount == 2:
        yyformat = ]b4_trans(["syntax error, unexpected {0}, expecting {1}"])[
      elif yycount == 3:
        yyformat = ]b4_trans(["syntax error, unexpected {0}, expecting {1} or {2}"])[
      elif yycount == 4:
        yyformat = ]b4_trans(["syntax error, unexpected {0}, expecting {1} or {2} or {3}"])[
      elif yycount == 5:
        yyformat = ]b4_trans(["syntax error, unexpected {0}, expecting {1} or {2} or {3} or {4}"])[
      self.yyerror(]b4_locations_if([[yyctx.location, ]])[yyformat.format(*yystr))
    else:
      self.yyerror(]b4_locations_if([[yyctx.location, ]])[]b4_trans(["syntax error"])[)]],
[simple], [[
    self.yyerror(]b4_locations_if([[yyctx.location, ]])[]b4_trans(["syntax error"])[)]])[

  @@classmethod
  def _yyPactValueIsDefault(cls, yyvalue: int) -> bool:
    """
     Whether the given <code>_yypact</code> value indicates a defaulted state.
     :param yyvalue: the value to check
    """
    return yyvalue == cls.__yypactninf

  @@classmethod
  def yyTableValueIsError(cls, yyvalue: int) -> bool:
    """
    Whether the given <code>_yytable</code> value indicates a syntax error.
    :param yyvalue: the value to check
    """
    return yyvalue == cls.__yypactninf

  __yypactninf: ]b4_int_type_for([b4_pact])[ = ]b4_pact_ninf[
  __yytableninf: ]b4_int_type_for([b4_table])[ = ]b4_table_ninf[

]b4_parser_tables_define[

]b4_parse_trace_if([[
  ]b4_integral_parser_table_define([rline], [b4_rline],
  [[YYRLINE[YYN] -- Source line where rule number YYN was defined.]])[

  def _yy_reduce_print(self, yyrule: int, yystack: _YYStack) -> None:
    """ Report on the debug stream that the rule yyrule is going to be reduced. """
    if self._yydebug == 0:
      return

    yylno: int = self._yyrline[yyrule]
    yynrhs: int = self._yyr2[yyrule]
    # Print the symbols being reduced, and their result.
    self.yycdebug("Reducing stack by rule {} (line {}):".format(
      yyrule - 1, yylno))

    # The symbols being reduced.
    for yyi in range(yynrhs):
      self._yy_symbol_print("   ${} =".format(yyi+1),
        SymbolKind(self._yystos[yystack.state_at(yynrhs - (yyi + 1))]),
        ]b4_rhs_data(yynrhs, yyi + 1)b4_locations_if([,
        b4_rhs_location(yynrhs, yyi + 1)])[)
]])[

  @@classmethod
  def _yytranslate(cls, t: int) -> SymbolKind:
    """
    YYTRANSLATE_(TOKEN-NUM) -- Symbol number corresponding to TOKEN-NUM
    as returned by yylex, with out-of-bounds checking.
    """
]b4_api_token_raw_if(dnl
[[
    return SymbolKind(t)
]],
[[
    CODE_MAX: int = ]b4_code_max[
    if t <= 0:
      return SymbolKind.]b4_symbol(0, kind)[
    elif t <= CODE_MAX:
      return SymbolKind(_yytranslate_table[t])
    else
      return SymbolKind.]b4_symbol(2, kind)[

]b4_integral_parser_table_define([translate_table], [b4_translate])[
]])[

  _YYLAST: int = ]b4_last[
  _YYEMPTY: int = -2
  _YYFINAL: int = ]b4_final_state_number[
  _YYNTOKENS: int = ]b4_tokens_number[

]b4_percent_code_get[
]b4_percent_code_get([[epilogue]])[]dnl
b4_epilogue[]dnl
b4_output_end
