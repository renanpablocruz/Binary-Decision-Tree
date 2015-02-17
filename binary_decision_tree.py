import impurity_measures as im
#import data_parser as dp

class BDTree(object):
	def __init__(self, class_label=None, tests=None, child_nodes=None):
		self.label = None
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
	 		if left_test.test_element(elem):
				return left_test.classify_element(elem)
			elif right_test.test_element(elem):
				return right_test.classify_element(elem)
			else:
				raise Exception("Element cannot be classified") # print something else to help debug

	def re_substituition_error(data):
		pass

	def generalization_error(data):
		pass

	def print_tree(self, level=0): # dfs
		prefix = "|"*level
		if self.label != None:
			print prefix, "label: ", self.label
		else:
			level += 1
			# print prefix, "att: ", self.attribute, self.left_test
			print prefix, "l", self.left_test
			self.left_node.print_tree(level)
			# print prefix, "att: ", self.attribute, self.right_test
			print prefix, "r", self.right_test
			self.right_node.print_tree(level)

# TODO: this function really belongs to here?
def build_tree(data, function, default_label):
	if data.all_elements_have_same_label():
			return BDTree(class_label=data.common_label())
	else:
		to_split, how_to_split = im.best_binary_split(data, function)
		if not to_split:
			return BDTree(class_label=default_label)
		else:
			_, [fv_A, fv_B], img = how_to_split
			dataset_A, dataset_B = data.split(fv_A, fv_B)
			return BDTree(tests=[fv_A, fv_B], child_nodes=[build_tree(dataset_A, function, default_label), build_tree(dataset_B, function, default_label)])
