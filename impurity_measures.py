from __future__ import division # all divisions are floating divisions
import contigency_table as ct
import utils as ut
from operator import itemgetter

'''
	This functions receive ContigencyTable (node) as arguments
	TODO: class to encapsulate the access to the data
	TODO: functions for discretizing
'''

def gini_node(node):
	return (1 - sum([x**2 for x in node.get_frequency()])/node.num_records()**2)

def gini_split(children_nodes):
	# children_nodes is a list of nodes(contigency tables) from the same feature
	sum_all_elements = sum([node.num_records() for node in children_nodes])
	return sum([node.num_records()*gini_node(node) for node in children_nodes]) / sum_all_elements

def gain_gini_split(parent, children_nodes):
	return gini_node(parent) - gini_split(children_nodes)

def entropy_node(node):
	n = node.num_records()
	return (-1)*sum([ut.xLog(x/n, 2) for x in node.get_frequency()])

def entropy_split(children_nodes):
	sum_all_elements = sum([node.num_records() for node in children_nodes])
	return sum([node.num_records()*entropy_node(node) for node in children_nodes]) / sum_all_elements

def gain_entropy_split(parent, children_nodes):
	return entropy_node(parent) - entropy_split(children_nodes)

def split_info(children_nodes):
	n = sum([node.num_records() for node in children_nodes])
	return (-1)*sum([ut.xLog(node.num_records()/n, 2) for node in children_nodes])

def gain_entropy_split_ratio(parent, children_nodes):
	a = gain_entropy_split(parent, children_nodes)
	b = split_info(children_nodes)
	return a / b

def misc_error_node(node):
	return 1 - max(node.get_frequency()) / node.num_records()

def misc_error_split(children_nodes):
	sum_all_elements = sum([node.num_records() for node in children_nodes])
	return sum([node.num_records()*misc_error_node(node) for node in children_nodes]) / sum_all_elements

def gain_misc_error_split(parent, children_nodes):
	return misc_error_node(parent) - misc_error_split(children_nodes)

def impurity_measure_node(function, node):
	if function == 'gini':
		return gini_node(node)
	elif function == 'info':
		return entropy_node(node)
	elif function == 'error':
		return misc_error_node(node)
	else:
		raise Exception('Not a valid function')

def impurity_measure_split(function, children_nodes):
	if function == 'gini':
		return gini_split(children_nodes)
	elif function == 'info':
		return entropy_split(children_nodes)
	elif function == 'error':
		return misc_error_split(children_nodes)
	else:
		raise Exception('Not a valid function')

def impurity_measure_gain(function, parent, children_nodes):
	if function == 'gini':
		return gain_gini_split(parent, children_nodes)
	elif function == 'info':
		return gain_entropy_split_ratio(parent, children_nodes)
	elif function == 'error':
		return gain_misc_error_split(parent, children_nodes)
	else:
		raise Exception('Not a valid function')

# given an attribute compute the best split or not split at all
# table is a list of nodes(contigency tables)
def split_categorical_argument(table, function, min_e_score = 0):
	#print table[0].feature ##################################################
	all_subsets = ut.powerset(table) # TODO: use indices instead of creating the subsets
	total_table = ct.sum_nodes(table)

	best_img = 0
	best_partition = ([], total_table) #TODO: optimize code removing unnecessary

	for setA in all_subsets:
		if(setA != table):
			setB = ut.diff(table, setA)
			img = impurity_measure_gain(function, total_table, [ct.sum_nodes(setA), ct.sum_nodes(setB)])
			if(img > best_img): # NOTE: probably the problem was here
				best_img = img
				best_partition = (ct.sum_nodes(setA), ct.sum_nodes(setB))

	if best_partition != ([], total_table):
		return (True, best_partition, best_img)
	else:
		return (False, best_partition, best_img)

def split_numeric_argument(table, function, min_e_score = 0):
	all_partitions = ut.partitions(table)
	total_table = ct.sum_nodes(table)

	best_img = 0
	best_partition = ([], total_table)

	for pt in all_partitions:
		img = impurity_measure_gain(function, total_table, [ct.sum_nodes(pt[0]), ct.sum_nodes(pt[1])])
		if(img > best_img):
				best_img = img
				best_partition = (ct.sum_nodes(pt[0]), ct.sum_nodes(pt[1]))

	if best_partition != ([], total_table):
		return (True, best_partition, best_img)
	else:
		return (False, best_partition, best_img)

def split_argument(type, table, function, min_e_score = 0):
	# if type == 'C':
	if type == 'C': # TODO: remember to fix this
		return split_categorical_argument(table, function)
	elif type == 'N':
		return split_numeric_argument(table, function)
	else:
		raise Exception("Not valid type of attribute", type)

# return the attribute to split and how to partitionate
# NOTE: kept for version control safety
def best_binary_split2(data, function):
	# TODO if all elements have the same class label, then not split and return this class label
	attributes = data.get_attribute_names()[:-1] # removing target class # TODO: encapsulate this
	types = data.get_attribute_types()[:-1]
	tables_by_attribute = [ct.contigency_tables_from_feature(att, data) for att in attributes] #TODO: encapsulate this???
	analysis_by_attribute = [split_categorical_argument(tables, function) for tables in tables_by_attribute]
	candidates_to_split = [analysis for analysis in analysis_by_attribute if analysis[0] == True] # if no attribute should be split?
	if len(candidates_to_split) == 0:
		return (False, [])
	else:
		best_candidate_to_split = sorted(candidates_to_split, key=itemgetter(2))[-1]
		return (True, best_candidate_to_split) # fix this return vale (booleans are redundant)

def best_binary_split(data, function):
	# TODO if all elements have the same class label, then not split and return this class label
	attributes = data.get_attribute_names()[:-1] # removing target class # TODO: encapsulate this
	types = dict(zip(attributes, data.get_attribute_types()[:-1]))
	tables_by_attribute = { att : ct.contigency_tables_from_feature(att, data) for att in attributes} #TODO: encapsulate this???
	analysis_by_attribute = [split_argument(types[att], tables_by_attribute[att], function) for att in attributes]
	candidates_to_split = [analysis for analysis in analysis_by_attribute if analysis[0] == True] # if no attribute should be split?
	if len(candidates_to_split) == 0:
		return (False, [])
	else:
		best_candidate_to_split = sorted(candidates_to_split, key=itemgetter(2))[-1]
		return (True, best_candidate_to_split) # fix this return vale (booleans are redundant)