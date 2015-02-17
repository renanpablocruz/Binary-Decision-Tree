import impurity_measures as im

class BDTNode(object):
	def __init__(self, class_label=None, tests=None, child_nodes=None):
		self.label = None
		self.left_test = None
		self.right_test = None
		self.left_node = None
		self.right_node = None
		if(class_label != None):
			self.label = class_label
		else:
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

class BDTree(object): # Binary Decision Tree
	def __init__(self, data, function, default_label):
		# refactor this
		# self.root = None
		# self.root = self.build_tree(root, data, function, default_label)
		boo, bcs = im.best_binary_split(data, function)
		while(boo):
			pass
		

	def classify_element(self, elem):
		return self.root.classify_element(elem)

	def print_tree(self):
		pass

	def build_tree(self, node, data, function, default_label):
		should_split, node, data_list = im.partition_data(data, function, default_label)
		if should_split == False:
			return BDTLabelNode(default_label)
		else:
			node.left_test = 