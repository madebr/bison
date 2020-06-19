# This Makefile is designed to be simple and readable.  It does not
# aim at portability.  It requires GNU Make.

BISON = bison
PROGS = simple

all: $(PROGS)

.PHONY: simple

simple: simple.py

%.py: %.y
	$(BISON) $(BISONFLAGS) -o $*.py $<

clean:
	rm -f $(PROGS:=.py)
