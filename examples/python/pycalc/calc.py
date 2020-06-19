from .driver import Driver
from typing import List


def main(args: List[str]) -> int:
  res = 0
  drv = Driver()
  for arg in args:
    if arg == "-p":
      drv.trace_parsing = True
    elif arg == "-s":
      drv.trace_scanning = True
    elif not drv.parse(arg):
      print(drv.result)
    else:
      res = 1
  return res


if __name__ == "__main__":
  import sys
  main(sys.argv)
