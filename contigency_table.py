from collections import Counter
import data_parser

class ContigencyTable(object):
	def __init__(self, feature, feature_values, class_labels):
		self.feature = feature
		self.feature_values = feature_values
		self.frequency = {label:0 for label in class_labels}
		# just to make checks
		self.class_labels = class_labels

	def __add__(self, other):
		# if self == None:
		# 	return other
		# if other == None:
		# 	return self
		if (self.feature != other.feature) or (self.class_labels != other.class_labels):
			raise Exception("Objects not compatible")
		else:
			# TODO: impprove this
			fv = list(self.feature_values) # copy of list
			fv.extend(other.feature_values)
			# print "$$$"
			# print self.feature_values
			# print "$$$"
			fv = list(set(fv))
			#print "fv: ", fv 
			r = ContigencyTable(self.feature, fv, self.class_labels)
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
		return elem[self.feature] in self.feature_values

	def print_in_tree(self):
		return self.feature + " " + str(self.feature_values)

###################################################################################################################
# functions for dealing with contigency tables
def contigency_tables_from_feature(feature, data):
	class_att = data.get_attribute_names()[-1]
	# print "class_att: ", class_att
	fv = data.get_values_of_attribute(feature)
	# print "attribute: ", feature
	# print "possible values:", fv
	cl = data.get_class_labels()
	tables = [ContigencyTable(feature, [v], cl) for v in fv]
	for elem in data.get_elements():
		feature_ins = elem[feature]
		for table in tables:
			if feature_ins in table.feature_values:
				table.compute(elem[class_att])
				break
		else:
			# TODO: remove this line from the final version
			#print "else"
			raise Exception("this instance has a feature value not computed")
	# for table in tables:
	# 	print table
	return tables

def sum_nodes(nodes):
	r = None
	# for node in nodes:
	# 	r += node
	# for i in range(0,len(nodes)):
	# 	if i==0:
	# 		r = nodes[0]
	# 	else:
	# 		r += nodes[i]
	for node in nodes:
		r += node
	if r==None: raise Exception("opa")
	return r