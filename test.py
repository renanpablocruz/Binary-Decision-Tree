import impurity_measures as im
import collections
import contigency_table as ct
import utils as ut
import data_parser as ps
import binary_decision_tree as bdt
import math

#from operator import itemgetter, attrgetter, methodcaller

#print data

# print type([1,'a'])
# print sum([1,2,3,4])**2
# print im.gini_node([[1], [2]])
# print im.gini_node(table1)
# print im.gini_node(table2)
# print im.gini_split([[('yes',5), ('no',2)], [('yes',1), ('no',4)]])
# print -sum([1])
# print im.entropy_node([('yes',0), ('no',6)])
# print im.entropy_node([('yes',1), ('no',5)])
# print im.entropy_node([('yes',2), ('no',4)])
# print im.entropy_split([[('yes',5), ('no',2)], [('yes',1), ('no',4)]])
# print 0 == -0
# print max([1,2,3])
# a = [1,2,3,4]
# a = a.reverse()
# b = [2,3]
# #print type(a)
# print im.xLog(2*2,2)

#print im.split_info(nodes)

#print im.diff([1,2,3], [2])

#print im.split_info(table)
#print isinstance([1], collections.Hashable)
#print im.split_categorical_argument(table, 'info')
# cl = ['C1', 'C2']
# a = ct.ContigencyTable('att', ['a'], cl)
# b = ct.ContigencyTable('att', ['b'], cl)
# for i in range (0,5): a.compute('C1')
# for i in range (0,2): a.compute('C2')
# for i in range (0,1): b.compute('C1')
# for i in range (0,4): b.compute('C2')
# print a.num_records()
# print a.get_frequency()
# print im.gini_node(a)
# print im.gini_node(b)
# print im.gini_split([a,b])
# a = ct.ContigencyTable('att', ['a'], cl)
# b = ct.ContigencyTable('att', ['b'], cl)
# for i in range (0,1): a.compute('C1')
# for i in range (0,5): a.compute('C2')
# for i in range (0,2): b.compute('C1')
# for i in range (0,4): b.compute('C2')
# print im.entropy_node(a)
# print im.entropy_node(b)
# print im.entropy_split([a,b]) == (im.entropy_node(a)+im.entropy_node(b))/2
# print im.misc_error_node(a)
# print im.misc_error_node(b)
# c = ct.contigency_tables_from_feature('marital status', data)
# [a,b,c] = ct.contigency_tables_from_feature('marital status', data)
# print 'c'
# for t in c:
# 	print t
# (boo, [a,b]) = im.split_categorical_argument(c, 'info')
# im.split_categorical_argument(c, 'info')
# print boo
# print a
# print b
# c = a+b
# print a
# print b
# print c
# d = [1,2,3]
# e = [3,4,5]
# d.extend(e)
# d = list(set(d))
# print "d: ", d
# print [1,2,3] != [1,2,2]
# for item in c:
# 	print item
# print ut.powerset([1,2,3,4])
# print list([1,2,3])
# print "#######"
# print a
# print b
# print c
# ct.sum_nodes([b,a])
# d = a+b
# print "#######"
# print a
# print b
# print c
dataset = ps.Dataset('dataset.data')
# print len(list(set([elem['class_size'] for elem in dataset.get_elements()])))

dataset2 = ps.Dataset('dataset2.csv')
# dataset2 = ps.Dataset('dataset.data')
# print dataset.get_class_labels()
# print dataset.get_attribute_names()
# print dataset.get_attribute_types()
# for elem in dataset.get_elements():
# 	print elem
# _, lt, _ = im.best_binary_split(dataset, 'info')
imf = 'info'
dl = '###'
# (boo, (_, (a, b), _)) = im.best_binary_split(dataset2, imf)
# # print "done"
# print "###"
# print a
# print "###"
# print b
# for t in lt:
# 	print t
# print [[k] for k in range(0,3)]
# print [3,5,8].index(3)
# print max([7.500000,3,4,8,9.0000000000])
# print sorted([(10,2), (5,4), (15,1)], key=itemgetter(1))
# btree = bdt.build_tree(dataset2, imf, dl)
# btree.print_tree()
# inf = float("inf")
# print inf*1
# a = [(1,0),(2,2),(3,3)]
# a[-1] = (a[-1][0], 4)
# print a
# disc = ut.get_bins_for_discretization([1,2,3,4,5,6,7,8,9,10], 3, 'equal_width')
# print disc
# print ut.discretized_value(3.5, disc)
# disc2 = ut.get_bins_for_discretization([1,2,3,4,5,6,7,8,9,10], 4, 'equal_freq')
# print disc2
# print ut.discretized_value(3.5, disc2)
dataset3 = ps.Dataset('sample1.csv')
# old_values = [elem['class_size'] for elem in dataset3.get_elements()]
# print old_values
# bins = ut.get_bins_for_discretization(old_values, 3, 'equal_width')
# print bins
# #dataset3.discretize_attribute('class_size', 3, 'equal_width')
dataset3.discretize_dataset(6, 'equal_width')
# new_values = [elem['class_size'] for elem in dataset3.get_elements()]
# print new_values
btree = bdt.build_tree(dataset3, imf, dl)
btree.print_tree()
# print type(math.floor(3.3))
# l = [1,2,3,4,5,5,6]
# n = 2
# print [l[i:i+n] for i in xrange(0, len(l), n)]
# print ut.partitions([1,2,3,4,5,6])
print list(set([9,0,45,4,2,7,1,2,3,89]))