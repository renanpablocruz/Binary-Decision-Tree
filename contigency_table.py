from __future__ import division # all divisions are floating divisions
from collections import Counter
import data_parser
import utils as ut

class ContigencyTable(object):
	def __init__(self, feature, feature_type, feature_values, class_labels):
		self.feature = feature
		self.feature_type = feature_type
		self.feature_values = feature_values
		self.frequency = {label:0 for label in class_labels}
		# just to make checks
		self.class_labels = class_labels

	def __add__(self, other):
		if (self.feature != other.feature) or (self.class_labels != other.class_labels):
			raise Exception("Objects not compatible")
		else:
			# TODO: improve this
			fv = list(self.feature_values) # copy of list
			fv.extend(other.feature_values)
			# print "$$$"
			# print self.feature_values
			# print "$$$"
			fv = sorted(list(set(fv)))
			#print "fv: ", fv 
			r = ContigencyTable(self.feature, self.feature_type, fv, self.class_labels)
			r.frequency = {label:(self.frequency[label] + other.frequency[label]) for label in self.class_labels}
			#print "r.freq: ", r.frequency
			return r

	def __radd__(self, other):
		if other == None:
			return self
		else:
			raise Exception("Not possible sum")

	def __str__(self):
		st1 = "feature: " + self.feature
		st2 = "\nfeature values:"
		# make better code
		for fv in self.feature_values:
			st2 = st2 + " " + str(fv) + ","
		st2 = st2[:-1]
		st3 = "\nfrequency:"
		for k,v in self.frequency.items():
			st3 = st3 + ' (' + k + ',' + str(v) + ')'
		return  st1 + st2 + st3

	def compute(self, class_label):
		self.frequency[class_label] = self.frequency[class_label] + 1

	def num_records(self):
		return sum([v for v in self.frequency.values()])

	def get_frequency(self):
		return [v for v in self.frequency.values()]

	def test_element(self, elem):
		att = self.feature
		att_type = self.feature_type
		if att_type == 'C':
			return elem[att] in self.feature_values
		elif att_type == 'N':
			return self.feature_values[0][0] <= elem[att] and elem[att] < self.feature_values[0][1]
		else:
			raise Exception("Invalid attribute type", att_type)

	def print_in_tree(self):
		return self.feature + " " + str(self.feature_values)

###################################################################################################################
# functions for dealing with contigency tables
def contigency_tables_from_feature(feature_name, feature_type, data):
	class_att = data.get_attribute_names()[-1]
	cl = data.get_class_labels()
	fv = data.get_values_of_attribute(feature_name)
	tables = [ContigencyTable(feature_name, feature_type, [v], cl) for v in fv]
	for elem in data.get_elements():
		feature_name_ins = elem[feature_name]
		for table in tables:
			if feature_name_ins in table.feature_values:
				table.compute(elem[class_att])
				break
		else:
			raise Exception("this instance has a invalid feature value")
	return tables

def sum_nodes(nodes):
	r = None
	for node in nodes:
		r += node
	if r==None: raise Exception("opa")
	return r

# create the appropriate numeric contigency table to add in the tree
def fix_numeric_contigency_tables(tableA, tableB):
	delim = (min(tableB.feature_values) + max(tableA.feature_values))/2
	if(delim <= 0):
		raise Exception("Numeric attributes not splitted correctly")
	else:
		# print "A", tableA.feature_values
		# print "B", tableB.feature_values
		tableA.feature_values = [(ut.n_inf, delim)]
		tableB.feature_values = [(delim, ut.p_inf)]
		return (tableA, tableB)