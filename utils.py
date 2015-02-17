from __future__ import division # all divisions are floating divisions
from itertools import *
import math

p_inf = float("inf")
n_inf = float("-inf")

def xLog(x, b):
	if x != 0:
		return x*math.log(x, b)
	else:
		return 0.0

def partition(seq, delim):
	return (seq[0:delim-1], seq[delim:])


def partitions(seq):
	return [(seq[0:n], seq[n:]) for n in range(1, len(seq))]

# def powerset(seq):
#  	return [x for x in powerset_generator(seq)]

# just include empty subset
def powerset(iterable):
    s = list(iterable)
    r = chain.from_iterable(combinations(s, r) for r in range(1,len(s)+1))
    return [list(x) for x in r]

def powerset_test(seq):
	print [x for x in powerset(seq)]

# def list_diff(list1, list2):
# 	return list(set(list1) - set(list2))

def diff(a, b):
	r = []
	for aa in a:
		include = True
		for bb in b:
			if aa == bb:
				include = False
				break
		if include:
			r.append(aa)
	return r

def check_equality_list(iterator):
      try:
         iterator = iter(iterator)
         first = next(iterator)
         return all(first == rest for rest in iterator)
      except StopIteration:
         return True

def chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]

def get_bins_for_discretization(elems, num_bins, method): # in the code the standard is 10 bins
	# suppose num_bins is positive integer
	if method == "equal_width":
		max_elem = max(elems)
		min_elem = min(elems)
		bin_width =  (max_elem - min_elem)/num_bins
		intervals = []
		intervals.append( (0, (n_inf, min_elem+bin_width)) )
		for i in range(1,num_bins):
			last_bin = intervals[-1]
			delim = last_bin[1][1]
			new_bin = (i, (delim, delim + bin_width))
			intervals.append(new_bin)
		last_bin = intervals[-1]
		intervals[-1] = (last_bin[0], (last_bin[1][0], p_inf))
	elif method == "equal_freq":
		# suppose needs to discretize
		s_l = sorted(elems)
		elems_by_bin = len(s_l)/num_bins
		small_chunks = chunks(s_l, int(elems_by_bin))
		delimiters = []
		for i in range(1, len(small_chunks)):
			delimiters.append((small_chunks[i-1][-1] + small_chunks[i][0])/2)
		intervals = []
		intervals.append((0,(n_inf, delimiters[0])))
		for i in range(1,len(delimiters)):
			intervals.append( (i, (delimiters[i-1], delimiters[i])) )
		intervals.append( (len(delimiters), (intervals[-1][1][1], p_inf)) )
	else:
		raise Exception("Not a valid discretize method")
	return intervals

def discretized_value(value, bins):
	for bin in bins:
		if value >= bin[1][0] and value < bin[1][1]:
			return bin[0]
	else:
		print 
		raise Exception("Not possible to discretize this value", value)
