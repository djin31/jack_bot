#!/usr/bin/python
import probs
import sys

print "pairs"
probs.get_pair(float(sys.argv[1]))
print "soft"
probs.get_soft(float(sys.argv[1]))

