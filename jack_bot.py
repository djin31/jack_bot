#!/usr/bin/python
import probs
import sys

prob_face = min(float(sys.argv[1]), 0.499)
dlr_probs = probs.set_dealer(prob_face)

#use -d flag for debug
if (sys.argv[-1]=="-d"):
	print ".\t2 3 4 5 6 7 8 9 F A"
probs.refresh()
probs.get_hard(prob_face, dlr_probs)
probs.get_soft(prob_face, dlr_probs)
probs.get_pair(prob_face, dlr_probs)
