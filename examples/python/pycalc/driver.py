from typing import Dict, Optional
from parser import Location, Parser

# FIXME: how to pass the prototype of yylex
# // Give Flex the prototype of yylex we want ...
# # define YY_DECL \
#   yy::parser::symbol_type yylex (driver& drv)
# // ... and declare it for the parser's sake.
# YY_DECL;


# Conducting the whole scanning and parsing of pycalc.
class Driver(object):
  def __init__(self):
    self.variables: Dict[str, int] = {
      "one": 1,
      "two": 2,
    }
    self.result: int = ...

    # The name of the file being parsed.
    self.file: Optional[str] = None
    # Whether to generate scanner debug traces.
    self.trace_parsing: bool = False
    # The token's location used by the scanner.
    self.location: XX.Location = XX.Location ()

  # Run the parser on file F. Return 0 on success.
  def parse(self, f: str) -> int:
    self.file = f
    self.location.initialize (self.file)
    self.scan_begin ()
    parse = Parser (self)
    parse.set_debug_level (self.trace_parsing)
    res = parse ()
    self.scan_end ()
    return res

  # Handling the scanner
  def scan_begin(self) -> None:
    pass
  def scan_end(self) -> None
    pass
