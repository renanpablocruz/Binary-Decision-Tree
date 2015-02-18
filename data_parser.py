import utils as ut
import math as math
import copy

''' the data in read and stored in a object from this class'''
class Dataset(object):
	def __init__(self, data_file=None):
		self.elements = []
		self.attribute_names = []
		self.attribute_types = []
		self.class_labels = []
		self.bins = {} # only for numeric values with num_feature_values > num_bins
		self.not_splitted_attributes = []
		if(data_file != None):
			with open(data_file,'r') as f:
				self.attribute_names = f.readline().strip('\n').split(',')
				self.not_splitted_attributes = copy.deepcopy(self.attribute_names[:-1])
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
		return list(self.attribute_names)

	def get_attribute_types(self):
		return list(self.attribute_types)

	def get_elements(self):
		return list(self.elements)

	def get_class_labels(self):
		return list(self.class_labels)

	def get_values_of_attribute(self, attribute):
		fv = set([])
		for elem in self.get_elements():
			fv.add(elem[attribute])
		return sorted(list(fv)) # it's already sorted

	def get_bins(self):
		return copy.deepcopy(self.bins)

	def get_not_splitted_attributes(self):
		return copy.deepcopy(self.not_splitted_attributes)

	def set_attribute_as_splitted(self, att):
		self.not_splitted_attributes.remove(att)

	def copy_with_no_elem(self):
		copy = Dataset()
		#self.elements
		copy.attribute_names = list(self.attribute_names) # copying a list
		copy.attribute_types = list(self.attribute_types)
		copy.class_labels = list(self.class_labels)
		copy.bins = list(self.bins)
		copy.not_splitted_attributes = list(self.not_splitted_attributes)
		return copy

	def transfer_elements(self, other, elements):
		for elem in elements:
			other.elements.append(elem)
			self.elements.remove(elem)

	def split(self, fv_A, fv_B):
		if fv_A.feature != fv_B.feature:
			raise Exception("partition doesn't have same feature", fv_A.feature, "!=", fv_B.feature)
		else:
			attribute = fv_B.feature
			fv = fv_B.feature_values
			# Refactor this function. It's too inefficient copying the dataset
			source = copy.deepcopy(self)
			dest = self.copy_with_no_elem()
			elems = []
			for elem in source.get_elements():
				if elem[attribute] in fv:
					elems.append(elem)
			source.transfer_elements(dest, elems)
			return (source, dest)

	def discretize_attribute(self, attribute, method, num_bins=10):
		# will alter for sure the dataset
		# the attribute must be numeric
		if len(set([elem[attribute] for elem in self.elements])) > num_bins:
			bins = ut.get_bins_for_discretization([elem[attribute] for elem in self.elements], num_bins, method)
			self.bins[attribute] = bins
			for elem in self.elements:
				elem[attribute] = ut.discretized_value(elem[attribute], bins)

	def discretize_attribute_given_bins(self, attribute, attribute_bins):
		for elem in self.elements:
			elem[attribute] = ut.discretized_value(elem[attribute], attribute_bins)

	def discretize_dataset(self, method, num_bins=10):
		for i in range(0, len(self.attribute_types[:-1])):
			if self.attribute_types[i] == 'N':
				self.discretize_attribute(self.attribute_names[i], method, num_bins)

	def discretize_dataset_given_bins(self, bins):
		for att in bins.keys():
			self.discretize_attribute_given_bins(att, bins[att])

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
		for i in range(0, len(self.attribute_types[:-1])):
			if self.attribute_types[i] == 'N':
				self.cast_to_float_attribute(self.attribute_names[i])

	def most_common_class_label(self):
		att = self.attribute_names[-1]
		lst = [elem[att] for elem in self.elements]
		return max(set(lst), key=lst.count)