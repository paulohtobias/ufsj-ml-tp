# -*- coding: utf-8 -*-

# Código adaptado de https://stackoverflow.com/a/1557906

import atexit
from time import clock

def log(elapsed):
	print elapsed

def endlog():
	end = clock()
	elapsed = end-start
	log(elapsed)

start = clock()
atexit.register(endlog)
