from __future__ import division # all divisions are floating divisions
import impurity_measures as im
import math
import contigency_table as ct
#import data_parser as dp

class BDTree(object):
	def __init__(self, default_label, class_label=None, tests=None, child_nodes=None):
		self.label = None
		self.default_label = default_label
		self.attribute = None
		self.left_test = None
		self.right_test = None
		self.left_node = None
		self.right_node = None
		if(class_label != None):
			self.label = class_label
		else:
			self.attribute = tests[0].feature
			self.left_test = tests[0]
			self.right_test = tests[1]
			self.left_node = child_nodes[0]
			self.right_node = child_nodes[1]

	def classify_element(self, elem):
	 	if self.label != None:
	 		return self.label
	 	else:
	 		if self.left_test.test_element(elem):
				return self.left_node.classify_element(elem)
			elif self.right_test.test_element(elem):
				return self.right_node.classify_element(elem)
			else:
				# raise Exception("Element cannot be classified", elem) # print something else to help debug
				return self.default_label

	def classification_error(self, data):
		class_attribute_id = data.attribute_names[-1]
		perc_wrong_classif = sum([1 for elem in data.get_elements() if self.classify_element(elem) != elem[class_attribute_id]]) / len(data.get_elements())
		return perc_wrong_classif

	def print_tree(self, level=0): # dfs
		prefix = "|"*level
		if self.label != None:
			print prefix, "(", self.label, ")"
		else:
			level += 1
			# print prefix, "att: ", self.attribute, self.left_test
			print prefix, self.left_test.print_in_tree()
			self.left_node.print_tree(level)
			# print prefix, "att: ", self.attribute, self.right_test
			print prefix, self.right_test.print_in_tree()
			self.right_node.print_tree(level)

# TODO: this function really belongs to here?
def build_tree(data, function, default_label, threshold, unique_split):
	if data.all_elements_have_same_label():
		return BDTree(default_label, class_label=data.common_label())
	else:
		to_split, how_to_split = im.best_binary_split(data, function, threshold, unique_split)
		if not to_split:
			return BDTree(default_label, class_label=data.most_common_class_label())
		else:
			_, [fv_A, fv_B], img = how_to_split
			dataset_A, dataset_B = data.split(fv_A, fv_B)
			if fv_A.feature_type == 'N':
				fv_A, fv_B = ct.fix_numeric_contigency_tables(fv_A, fv_B)
			left_tree = build_tree(dataset_A, function, default_label, threshold, unique_split)
			right_tree = build_tree(dataset_B, function, default_label, threshold, unique_split)
			return BDTree(default_label, tests=[fv_A, fv_B], child_nodes=[left_tree, right_tree])

def helper_MDL_tree(btree, log2n, log2k):
	if btree.label != None:
		return log2k
	else:
		return log2n + helper_MDL_tree(btree.left_node, log2n, log2k) + helper_MDL_tree(btree.right_node, log2n, log2k)

def MDL_tree(btree, data):
	n = len(data.get_attribute_names()[:-1])
	k = len(data.get_class_labels())
	log2n = math.log(n,2)
	log2k = math.log(k,2)
	return helper_MDL_tree(btree, log2n, log2k)

def MDL_data(btree, data):
	m = len(data.get_elements())
	k = len(data.get_class_labels())
	log2mk = math.log(m*k, 2)
	class_attribute_id = data.attribute_names[-1]
	return log2mk*sum([1 for elem in data.get_elements() if btree.classify_element(elem) != elem[class_attribute_id]])

def MDL(btree, data):
	return MDL_tree(btree, data) + MDL_data(btree, data)