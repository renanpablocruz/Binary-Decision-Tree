import utils as ut

''' the data in read and stored in a object from this class'''
class Dataset(object):
	def __init__(self, data_file=None):
		self.elements = []
		self.attribute_names = []
		self.attribute_types = []
		self.class_labels = []
		self.bins = [] # only for numeric values with num_feature_values > num_bins
		# TODO: the numeric values should be saved as float
		# TODO AFTER: remove float() from discretize_attribute
		if(data_file != None):
			with open(data_file,'r') as f:
				self.attribute_names = f.readline().strip('\n').split(',')
				# todo: standardize class 
				self.attribute_types = f.readline().strip('\n').split(',')
				# print attribute_names
				# print attribute_types
				cl = set([])
				for line in f:
					line_info = line.strip('\n').split(',')
					self.elements.append(dict(zip(self.attribute_names, line_info)))
					cl.add(line_info[-1])
				self.class_labels = list(cl)
		self.cast_to_float_numeric_attributes()

	def get_attribute_names(self):
		return self.attribute_names

	def get_attribute_types(self):
		return self.attribute_types

	def get_elements(self):
		return self.elements

	def get_class_labels(self):
		return self.class_labels

	def get_values_of_attribute(self, attribute):
		fv = set([])
		for elem in self.get_elements():
			fv.add(elem[attribute])
		return list(fv) # it's already sorted

	def create_copy_with_elem(self): # TODO: probably will become with specific elements
		copy = Dataset()
		copy.attribute_names = list(self.attribute_names) # copying a list
		copy.attribute_types = list(self.attribute_types)
		copy.class_labels = list(self.class_labels)
		return copy

	def remove_elements(self, elements):
		datasetB = self.create_copy_with_elem()
		for elem in elements:
			self.elements.remove(elem)

	def transfer_elements(self, other, elements):
		for elem in elements:
			other.elements.append(elem)
			self.elements.remove(elem)

	def split(self, fv_A, fv_B):
		attribute = fv_B.feature
		fv = fv_B.feature_values
		# Refactor this function. It's too inefficient copy the dataset
		copy = self.create_copy_with_elem()
		elems = []
		for elem in self.elements:
			if elem[attribute] in fv:
				elems.append(elem)
		self.transfer_elements(copy, elems)
		return [self, copy]

	def discretize_attribute(self, attribute, num_bins, method):
		# will alter for sure the dataset
		# the attribute must be numeric
		if len(set([elem[attribute] for elem in self.elements])) > num_bins:
			bins = ut.get_bins_for_discretization([elem[attribute] for elem in self.elements], num_bins, method)
			self.bins.append({attribute:bins})
			for elem in self.elements:
				elem[attribute] = ut.discretized_value(elem[attribute], bins)

	def discretize_dataset(self, num_bins, method):
		for i in range(0, len(self.attribute_types)):
			if self.attribute_types[i] == 'N':
				self.discretize_attribute(self.attribute_names[i], num_bins, method)

	def all_elements_have_same_label(self):
		# print "@@@@@@@@@@@@@@@", self.attribute_names[-1], "@@@@@@@@@@@@@@@@@@"
		# print [elem[self.attribute_names[-1]] for elem in self.elements]
		return ut.check_equality_list([elem[self.attribute_names[-1]] for elem in self.elements])

	def common_label(self): # can only be called if all_elements_have_same_label returned true
		return self.elements[0][self.attribute_names[-1]]

	def cast_to_float_attribute(self, attribute):
		for elem in self.elements:
			elem[attribute] = float(elem[attribute])

	def cast_to_float_numeric_attributes(self):
		for i in range(0, len(self.attribute_types)):
			if self.attribute_types[i] == 'N':
				self.cast_to_float_attribute(self.attribute_names[i])