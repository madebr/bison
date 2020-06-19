                                                            -*- Autoconf -*-

# Python language support for Bison

# Copyright (C) 2020-2020 Free Software Foundation, Inc.

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

# _b4_comment(TEXT, OPEN, CONTINUE, END)
# --------------------------------------
# Put TEXT in comment.  Avoid trailing spaces: don't indent empty lines.
# Avoid adding indentation to the first line, as the indentation comes
# from OPEN.  That's why we don't patsubst([$1], [^\(.\)], [   \1]).
#
# Prefix all the output lines with PREFIX.
m4_define([_b4_comment],
[$2[]m4_bpatsubst(m4_expand([[$1]]), [
\(.\)], [
$3\1])$4])

# b4_comment(TEXT, [PREFIX])
# --------------------------
# Put TEXT in comment.  Prefix all the output lines with PREFIX.
m4_define([b4_comment],
[_b4_comment([$1], [$2# ], [$2# ], [$2# ])])


# b4_list2(LIST1, LIST2)
# ----------------------
# Join two lists with a comma if necessary.
m4_define([b4_list2],
          [$1[]m4_ifval(m4_quote($1), [m4_ifval(m4_quote($2), [[, ]])])[]$2])


# b4_percent_define_get3(DEF, PRE, POST, NOT)
# -------------------------------------------
# Expand to the value of DEF surrounded by PRE and POST if it's %define'ed,
# otherwise NOT.
m4_define([b4_percent_define_get3],
          [m4_ifval(m4_quote(b4_percent_define_get([$1])),
                [$2[]b4_percent_define_get([$1])[]$3], [$4])])



# b4_flag_value(BOOLEAN-FLAG)
# ---------------------------
m4_define([b4_flag_value], [b4_flag_if([$1], [True], [False])])


# b4_parser_class_declaration
# ---------------------------
# The declaration of the parser class ("class YYParser"), with all its
# qualifiers/annotations.

m4_define([b4_parser_class_declaration],
[b4_percent_define_get3([api.parser.annotations], [], [ ])dnl
[class ]b4_parser_class[]dnl
b4_percent_define_get3([api.parser.extends], [ extends ])[:]])
# FIXME: convert to comma seperated list inside braces




# b4_lexer_if(TRUE, FALSE)
# ------------------------
m4_define([b4_lexer_if],
[b4_percent_code_ifdef([[lexer]], [$1], [$2])])


# b4_identification
# -----------------
m4_define([b4_identification],
[
  # Version number for the Bison executable that generated this parser.
  BISON_VERSION = "b4_version"

  # Name of the skeleton that generated this parser.
  BISON_SKELETON = b4_skeleton
])


## ------------ ##
## Typing       ##
## ------------ ##

# b4_list(TYPE)
# ---------------------
# Wrap TYPE between List:
# List[$TYPE]
m4_define([b4_list], [[List[$1]]])

# b4_optional(TYPE)
# ---------------------
# Wrap TYPE between Optional:
# Optional[$TYPE]
m4_define([b4_optional], [[Optional[$1]]])

# b4_tuple(TYPES)
# ---------------------
# Wrap TYPES between Tuple:
# Tuple[$TYPES]
m4_define([b4_tuple], [[Tuple[$1]]])

# b4_tuple_vararg(TYPE)
# ---------------------
# Wrap TYPE between Tuple:
# Tuple[$TYPES]
m4_define([b4_tuple_vararg], [[Tuple[$1, ...]]])

# b4_union(TYPES)
# ---------------------
# Wrap TYPES between Union:
# Union[$TYPE]
m4_define([b4_union], [[Union[$1]]])




## ------------ ##
## Data types.  ##
## ------------ ##

# b4_int_type(MIN, MAX)
# ---------------------
# Return the smallest int type able to handle numbers ranging from
# MIN to MAX (included).
m4_define([b4_int_type], [int])

# b4_int_type_for(NAME)
# ---------------------
# Return the smallest int type able to handle numbers ranging from
# 'NAME_min' to 'NAME_max' (included).
m4_define([b4_int_type_for],
[b4_int_type($1_min, $1_max)])

# b4_null
# -------
m4_define([b4_null], [None])


# b4_typed_parser_table_define(TYPE, NAME, DATA, COMMENT)
# -------------------------------------------------------
m4_define([b4_typed_parser_table_define],
[m4_ifval([$4], [
b4_comment([$4], [  ])
])dnl
[  _yy$2: ]b4_tuple_vararg($1)[ = (
  ]$3[
  )]])


# b4_integral_parser_table_define(NAME, DATA, COMMENT)
#-----------------------------------------------------
m4_define([b4_integral_parser_table_define],
[b4_typed_parser_table_define([b4_int_type_for([$2])], [$1], [$2], [$3])])


## ------------- ##
## Token kinds.  ##
## ------------- ##


# b4_token_enum(TOKEN-NUM)
# ------------------------
# Output the definition of this token as an enum.
m4_define([b4_token_enum],
[b4_token_visible_if([$1],
    [m4_format([[    """ Token %s, to be returned by the scanner.  """
    %s: int = %s%s
]],
               b4_symbol([$1], [tag]),
               b4_symbol([$1], [id]),
               b4_symbol([$1], b4_api_token_raw_if([[number]], [[code]])))])])


# b4_token_enums
# --------------
# Output the definition of the tokens (if there are) as enums.
m4_define([b4_token_enums],
[b4_any_token_visible_if([    # Token kinds.
b4_symbol_foreach([b4_token_enum])])])



## -------------- ##
## Symbol kinds.  ##
## -------------- ##


# b4_symbol_kind(NUM)
# -------------------
m4_define([b4_symbol_kind],
[b4_symbol_kind_base($@)])


# b4_symbol_enum(SYMBOL-NUM)
# --------------------------
# Output the definition of this symbol as an enum.
m4_define([b4_symbol_enum],
[m4_format([    %-30s %s],
           m4_format([[%s = %s%s]],
                     b4_symbol([$1], [kind_base]),
                     [$1],
                     m4_if([$1], b4_last_symbol, [[,]], [[,]])),
           [b4_symbol_tag_comment([$1])])])


# b4_declare_symbol_enum
# ----------------------
# The definition of the symbol internal numbers as an enum.
m4_define([b4_declare_symbol_enum],
[[  class SymbolKind(IntEnum):
]b4_symbol_foreach([b4_symbol_enum])[

    _VALUES = (
      ]m4_map_args_sep([b4_symbol_kind(], [)], [,
      ], b4_symbol_numbers)[,
    )

]b4_parse_error_bmatch(
[simple\|verbose],
[[    # Return YYSTR after stripping away unnecessary quotes and
    # backslashes, so that it's suitable for yyerror.  The heuristic is
    #  that double-quoting is unnecessary unless the string contains an
    #  apostrophe, a comma, or backslash (other than backslash-backslash).
    #  YYSTR is taken from yytname.
    @@staticmethod
    def _yytnamerr(yystr: str) -> str:
      if yystr[0] == '"':
        yyr = []
        i = 1
        while i < len(yystr):
          c = yystr[i]
          if c == "\'" or c == ",":
            break
          if c == "\\":
            i += 1
            c = yystr[i]
            if c != '\\':
              break
          yyr.append(c)
          if c == "\"":
            return "".join(yyr)
      return yystr

    # YYNAMES_[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
    # First, the terminals, then, starting at \a YYNTOKENS_, nonterminals.
    _YYNAMES = (
  ]b4_symbol_names[)][

    @@property
    def name(self) -> str:
      """The user-facing name of this symbol."""
      return self._YYNAMES[self.value]
]],
[custom\|detailed],
[[    # YYNAMES_[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
    # First, the terminals, then, starting at \a YYNTOKENS_, nonterminals.
    _YYNAMES = (
  ]b4_symbol_names[)][

    @@property
    def name(self):
      """The user-facing name of this symbol."""
      return self._YYNAMES[self.value]
]])])])



# b4_case(ID, CODE, [COMMENTS])
# -----------------------------
m4_define([b4_case],
[
      if yyn == $1:m4_ifval([$3], [ b4_comment([$3])])
        $2
        break
])


# b4_predicate_case(LABEL, CONDITIONS)
# ------------------------------------
m4_define([b4_predicate_case],
[  case $1:
     if (! ($2)) YYERROR;
    break;
])


## -------- ##
## Checks.  ##
## -------- ##

b4_percent_define_check_kind([[api.value.type]],    [code], [deprecated])

b4_percent_define_check_kind([[annotations]],       [code], [deprecated])
b4_percent_define_check_kind([[extends]],           [code], [deprecated])
b4_percent_define_check_kind([[implements]],        [code], [deprecated])
b4_percent_define_check_kind([[init_throws]],       [code], [deprecated])
b4_percent_define_check_kind([[lex_throws]],        [code], [deprecated])
b4_percent_define_check_kind([[api.parser.class]],  [code], [deprecated])
b4_percent_define_check_kind([[throws]],            [code], [deprecated])



## ---------------- ##
## Default values.  ##
## ---------------- ##

m4_define([b4_yystype], [b4_percent_define_get([[api.value.type]])])
b4_percent_define_default([[api.value.type]], [[object]])
b4_percent_define_default([[api.symbol.prefix]], [[S_]])

# b4_api_prefix, b4_api_PREFIX
# ----------------------------
# Corresponds to %define api.prefix
b4_percent_define_default([[api.prefix]], [[YY]])
m4_define([b4_api_prefix],
[b4_percent_define_get([[api.prefix]])])
m4_define([b4_api_PREFIX],
[m4_toupper(b4_api_prefix)])

# b4_prefix
# ---------
# If the %name-prefix is not given, it is api.prefix.
m4_define_default([b4_prefix], [b4_api_prefix])

b4_percent_define_default([[api.parser.class]], [b4_prefix[]Parser])
m4_define([b4_parser_class], [b4_percent_define_get([[api.parser.class]])])

b4_percent_define_default([[lex_throws]], [[java.io.IOException]])
m4_define([b4_lex_throws], [b4_percent_define_get([[lex_throws]])])

b4_percent_define_default([[throws]], [])
m4_define([b4_throws], [b4_percent_define_get([[throws]])])

b4_percent_define_default([[init_throws]], [])
m4_define([b4_init_throws], [b4_percent_define_get([[init_throws]])])

b4_percent_define_default([[api.location.type]], [Location])
m4_define([b4_location_type], [b4_percent_define_get([[api.location.type]])])
m4_define([b4_location_type_full], [b4_parser_class[.]b4_location_type])

b4_percent_define_default([[api.position.type]], [Position])
m4_define([b4_position_type], [b4_percent_define_get([[api.position.type]])])
m4_define([b4_position_type], [b4_percent_define_get([[api.position.type]])])


## ----------------- ##
## Semantic Values.  ##
## ----------------- ##


# b4_symbol_translate(STRING)
# ---------------------------
# Used by "bison" in the array of symbol names to mark those that
# require translation.
m4_define([b4_symbol_translate],
[[i18n($1)]])


# b4_trans(STRING)
# ----------------
# Translate a string if i18n is enabled.  Avoid collision with b4_translate.
m4_define([b4_trans],
[b4_has_translations_if([i18n($1)], [$1])])



# b4_symbol_value(VAL, [SYMBOL-NUM], [TYPE-TAG])
# ----------------------------------------------
# See README.
m4_define([b4_symbol_value],
[m4_ifval([$3],
          [(($3)($1))],
          [m4_ifval([$2],
                    [b4_symbol_if([$2], [has_type],
                                  [((b4_symbol([$2], [type]))($1))],
                                  [$1])],
                    [$1])])])


# b4_lhs_value([SYMBOL-NUM], [TYPE])
# ----------------------------------
# See README.
m4_define([b4_lhs_value], [yyval])


# b4_rhs_data(RULE-LENGTH, POS)
# -----------------------------
# See README.
m4_define([b4_rhs_data],
[yystack.value_at (b4_subtract($@))])

# b4_rhs_value(RULE-LENGTH, POS, SYMBOL-NUM, [TYPE])
# --------------------------------------------------
# See README.
#
# In this simple implementation, %token and %type have class names
# between the angle brackets.
m4_define([b4_rhs_value],
[b4_symbol_value([b4_rhs_data([$1], [$2])], [$3], [$4])])


# b4_lhs_location()
# -----------------
# Expansion of @$.
m4_define([b4_lhs_location],
[(yyloc)])


# b4_rhs_location(RULE-LENGTH, POS)
# ---------------------------------
# Expansion of @POS, where the current rule has RULE-LENGTH symbols
# on RHS.
m4_define([b4_rhs_location],
[yystack.location_at (b4_subtract($@))])


# b4_lex_param
# b4_parse_param
# --------------
# If defined, b4_lex_param arrives double quoted, but below we prefer
# it to be single quoted.  Same for b4_parse_param.

# TODO: should be in bison.m4
m4_define_default([b4_lex_param], [[]])
m4_define([b4_lex_param], b4_lex_param)
m4_define([b4_parse_param], b4_parse_param)

# b4_lex_param_decl
# -----------------
# Extra formal arguments of the constructor.
m4_define([b4_lex_param_decl],
[m4_ifset([b4_lex_param],
          [b4_remove_comma([$1],
                           b4_param_decls(b4_lex_param))],
          [$1])])

m4_define([b4_param_decls],
          [m4_map([b4_param_decl], [$@])])
m4_define([b4_param_decl], [, $1])

m4_define([b4_remove_comma], [m4_ifval(m4_quote($1), [$1, ], [])m4_shift2($@)])



# b4_parse_param_decl
# -------------------
# Extra formal arguments of the constructor.
m4_define([b4_parse_param_decl],
[m4_ifset([b4_parse_param],
          [b4_remove_comma([$1],
                           b4_param_decls(b4_parse_param))],
          [$1])])



# b4_lex_param_call
# -----------------
# Delegating the lexer parameters to the lexer constructor.
m4_define([b4_lex_param_call],
          [m4_ifset([b4_lex_param],
                    [b4_remove_comma([$1],
                                     b4_param_calls(b4_lex_param))],
                    [$1])])
m4_define([b4_param_calls],
          [m4_map([b4_param_call], [$@])])
m4_define([b4_param_call], [, $2])



# b4_parse_param_cons
# -------------------
# Extra initialisations of the constructor.
m4_define([b4_parse_param_cons],
          [m4_ifset([b4_parse_param],
                    [b4_constructor_calls(b4_parse_param)])])

m4_define([b4_constructor_calls],
          [m4_map([b4_constructor_call], [$@])])
m4_define([b4_constructor_call],
          [this.$2 = $2;
          ])



# b4_parse_param_vars
# -------------------
# Extra instance variables.
m4_define([b4_parse_param_vars],
          [m4_ifset([b4_parse_param],
                    [
    /* User arguments.  */
b4_var_decls(b4_parse_param)])])

m4_define([b4_var_decls],
          [m4_map_sep([b4_var_decl], [
], [$@])])
m4_define([b4_var_decl],
          [    protected final $1;])



# b4_maybe_throws(THROWS)
# -----------------------
# Expand to either an empty string or "throws THROWS".
m4_define([b4_maybe_throws],
          [m4_ifval($1, [ throws $1])])
