# Load libraries
import math
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import operator
from sklearn.metrics import confusion_matrix

import pydotplus

import pygraphviz as pgv

G = pgv.AGraph(directed=True)


def entropy(attr_name):
    entropy = 0
    row_del_dict = dict()
    inner_row_del_dict = dict()
    # getting column contents of current attribute name from data extracted from csv file
    attr_list = list(data[attr_name])
    if attr_name == 'fast':
        # get number of unique classes in attribute
        class_attr_list = set(attr_list)
        all_classes = list(class_attr_list)  # convert back to list
        # print(all_classes)
        for x in all_classes:
            probability = attr_list.count(x)/len(attr_list)
            entropy -= (probability*math.log2(probability))
            # print(len(attr_list))
    else:
        merged_class = list(zip(attr_list, list(data['fast'])))
        # entropy=0
        # get number of unique classes in attribute
        class_attr_list = set(merged_class)
        all_classes = list(class_attr_list)  # convert back to list
        # uniq_list=unique_attr_clases(attr_list)
        # print(all_classes)
        for x in all_classes:
            probability = merged_class.count(x)/attr_list.count(x[0])
            # print(attr_list.count(x[0]),len(attr_list),probability,math.log2(probability))
            # entropy of child combinations
            sub_entropy = probability*math.log2(probability)
            # dictionary to determine rows to be deleted in table reduction
            inner_row_del_dict[x[0]] = sub_entropy
            row_del_dict[attr_name] = inner_row_del_dict
            entropy -= (attr_list.count(x[0])/len(attr_list))*(sub_entropy)

    #print("Target Attribute Entropy: ",entropy, "\n")
    return entropy, row_del_dict


def information_gain(target_entopy, attr_entopy):
    info_gain = target_entopy-attr_entopy
    return info_gain


def root_node_election(target_entopy):
    rst_dict = dict()
    for x in data_headers[:-1]:  # calculate entopies of all minus the target
        print("Entropy of ", x, " is ", entropy(x))
        attr_entopy, attr_row_del_dict = entropy(x)
        info_gain = information_gain(target_entopy, attr_entopy)

        print("IG of ", x, " is ", info_gain)
        # store results in a dictionary
        rst_dict[x] = info_gain, attr_row_del_dict
    # print(print(max(rst_dict.items(),key=operator.itemgetter(1))[0]))
    # print(attr_entopy)
    # print(attr_row_del_dict)
    max_col = max(rst_dict.items(), key=operator.itemgetter(1))[0]
    del_row = max(rst_dict.items(), key=operator.itemgetter(1))[1]
    # for p_id, p_info in del_row.items():
    #    print("\nPerson ID:", p_id)
    #   for key in p_info:
    #      print(key + ':', del_row[key])
    #print('Values are', del_row[1])
    #print("Those to delete are",del_row[1])
    # return max(rst_dict.items(),key=operator.itemgetter(1))[0],attr_row_del_dict
    return max_col, del_row[1]


# training data table reduction for next iteration
def reduce_training_dataset(data, delete_rows, selected_root_node):

    for item in delete_rows:
        data = data[data.eval(selected_root_node) != item]
        print(data)
    data = data.drop(selected_root_node, axis=1)
    # print(data.head(0))
    # delete header of choosen root node
    data_headers.remove(selected_root_node)
    return data


# code loads from here
# using pandas to read csv file containing training dataset
# data_headers=['engine','turbo','weight','fueleco','fast']
data_headers = ['engine', 'turbo', 'weight', 'fueleco', 'fast']
# data=pd.read_csv("id3_data.csv",names=data_headers,header=None)
data = pd.read_csv("data.csv", names=data_headers, header=None)
# print(entropy(list(data['fast'])))
print


# First Iteration
# for i in range(4):
target_entopy, attr_row_del_dict = entropy('fast')
print("Entropy of fast is: ", target_entopy)
selected_root_node, delete_rows = root_node_election(target_entopy)
G.add_node(selected_root_node, color='red')
print("Smaller entopies of root node are: ", delete_rows)
# print(delete_rows[selected_root_node].items())
delete_row = []
for row, value in delete_rows[selected_root_node].items():
    G.add_node(row, color='blue')
    G.add_edge(selected_root_node, row, color='blue')
    print(row)
    if value == 1 or value == 0:  # arrest values with extreem entopies
        delete_row.append(row)  # store them in a list
print("The selected root node is: ", selected_root_node)
print("The rows to be deleted are: ", delete_row)
data = reduce_training_dataset(data, delete_row, selected_root_node)
print("New data set for next iteration is: \n", data)




target_entopy, attr_row_del_dict = entropy('fast')
print("Entropy of fast is: ", target_entopy)
selected_root_node, delete_rows = root_node_election(target_entopy)
G.add_node(selected_root_node, color='red')
G.add_edge(row,selected_root_node, color='blue')
print("Smaller entopies of root node are: ", delete_rows)
# print(delete_rows[selected_root_node].items())
delete_row = []
for row, value in delete_rows[selected_root_node].items():
    G.add_node(row, color='blue')
    G.add_edge(selected_root_node, row, color='blue')
    print(row)
    if value == 1 or value == 0:  # arrest values with extreem entopies
        delete_row.append(row)  # store them in a list
print("The selected root node is: ", selected_root_node)
print("The rows to be deleted are: ", delete_row)
data = reduce_training_dataset(data, delete_row, selected_root_node)
print("New data set for next iteration is: \n", data)




target_entopy, attr_row_del_dict = entropy('fast')
print("Entropy of fast is: ", target_entopy)
selected_root_node, delete_rows = root_node_election(target_entopy)
G.add_node(selected_root_node, color='red')
G.add_edge(row,selected_root_node, color='blue')
print("Smaller entopies of root node are: ", delete_rows)
# print(delete_rows[selected_root_node].items())
delete_row = []
for row, value in delete_rows[selected_root_node].items():
    G.add_node(row, color='blue')
    G.add_edge(selected_root_node, row, color='blue')
    print(row)
    if value == 1 or value == 0:  # arrest values with extreem entopies
        delete_row.append(row)  # store them in a list
print("The selected root node is: ", selected_root_node)
print("The rows to be deleted are: ", delete_row)
data = reduce_training_dataset(data, delete_row, selected_root_node)
print("New data set for next iteration is: \n", data)




target_entopy, attr_row_del_dict = entropy('fast')
print("Entropy of fast is: ", target_entopy)
selected_root_node, delete_rows = root_node_election(target_entopy)
G.add_node(selected_root_node, color='red')
G.add_edge(row,selected_root_node, color='blue')
print("Smaller entopies of root node are: ", delete_rows)
# print(delete_rows[selected_root_node].items())
delete_row = []
for row, value in delete_rows[selected_root_node].items():
    G.add_node(row, color='blue')
    G.add_edge(selected_root_node, row, color='blue')
    print(row)
    if value == 1 or value == 0:  # arrest values with extreem entopies
        delete_row.append(row)  # store them in a list
print("The selected root node is: ", selected_root_node)
print("The rows to be deleted are: ", delete_row)
data = reduce_training_dataset(data, delete_row, selected_root_node)
print("New data set for next iteration is: \n", data)



  




# write to a dot file
G.write('test.dot')

# create a png file
G.layout(prog='dot')  # use dot
G.draw('file.png')
# construct_decision_tree(selected_root_node)
