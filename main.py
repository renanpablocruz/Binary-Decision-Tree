#!/usr/bin/env python
# check correctness of input
# execute code

import sys
import data_parser as ps
import binary_decision_tree as bdt

def main(training_data, testing_data, split_function, threshold):
	training_set = ps.Dataset(training_data)
	training_set.discretize_dataset('equal_width') # how to decide this?
	btree = bdt.build_tree(training_set, split_function, '###', threshold)

	testing_set = ps.Dataset(testing_data)
	testing_set.discretize_dataset_given_bins(training_set.get_bins())

	# # re-substituition
	# print "Re-subsitution error:", btree.classification_error(training_set)
	# # generalization
	# print "Generalization error:", btree.classification_error(testing_set)
	# # MDL
	# print "MDL:","x","bits"
	# the data is split while the impurity_measure_gain is bigger than the threshold

	btree.print_tree2()

	# re-substituition
	print "Re-subsitution error:", "{0:.2f}".format(btree.classification_error(training_set)*100), "%"
	# generalization
	print "Generalization error:", "{0:.2f}".format(btree.classification_error(testing_set)*100), "%"
	# MDL
	# Only training set was used
	print "MDL:", "{0:.2f}".format(bdt.MDL(btree, training_set)), "bits"

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]))