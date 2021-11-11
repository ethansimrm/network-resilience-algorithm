## Application 2: Analysis of a Computer Network

import user48_E90mZSM3mM_16 as proj_2
import alg_application2_provided as algo
import random
import codeskulptor
codeskulptor.set_timeout(60)

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"

network_data = algo.load_graph(NETWORK_URL)

## Question 1

# Algorithm ER for undirected graphs

def ER(num_nodes, prob):
    ans_dict = {}
    for node in range(num_nodes):
        ans_dict[node] = set([])
    for node in range(num_nodes):
        for tail_node in range(node + 1, num_nodes):
            if node != tail_node:
                a = random.random()
                if a < prob:
                    ans_dict[node].add(tail_node)
                    ans_dict[tail_node].add(node)
    return ans_dict

# Issue: We considered each edge twice, e.g. in a ugraph with 2 nodes,
# we trial 0, then 1 to see if we have the edge 0<->1. But if we fail this trial,
# we trial 1, then 0 again! We should not be doing this!

# UPA algorithm

import alg_upa_trial as provided

# Seems like the UPA algorithm generates a complete 
# undirected graph, and slowly builds
# towards the desired graph node by node;
# each node adds edges in steps.

def make_complete_ugraph(num_nodes):
    """
    Generates a complete undirected
    graph for a given number of nodes.
    
    Returns graph in dictionary form.
    """
    ans_dict = {}
    if num_nodes > 0:
        for node in range(num_nodes):
            ans_dict[node] = set([])
        for node in range(num_nodes):
            for tail in range(num_nodes):
                if tail != node:
                    ans_dict[node].add(tail)
                    ans_dict[tail].add(node)
    return ans_dict

def upa(num_nodes, final_nodes):
    complete_upa = provided.UPATrial(num_nodes)
    ans_dict = make_complete_ugraph(num_nodes)
    for node in range(num_nodes, final_nodes):
        new_neighs = complete_upa.run_trial(num_nodes)
        ans_dict[node] = set([])
        for neigh in new_neighs:
            ans_dict[node].add(neigh)
            ans_dict[neigh].add(node)
    return ans_dict

def count_edges(ugraph):
    """
    Counts edges in an undirected graph. Returns integer.
    """
    counter = 0
    for edge_set in ugraph.values():
        for element in edge_set:
            counter += 1
    return float(counter) / 2

er_data = ER(1239, 0.004)

# Probability p is 0.004 for ER graph.

upa_data = upa(3, 1239)

# Integer m is 3 for UPA graph.

def random_order(ugraph):
    """
    Takes an undirected graph ugraph and returns a list
    of nodes in the graph in some random order.
    """
    node_list = ugraph.keys()
    random.shuffle(node_list)
    return node_list
              
#attack_network = random_order(network_data)
#attack_er = random_order(er_data)
#attack_upa = random_order(upa_data)
#
#network_res = proj_2.compute_resilience(network_data, attack_network)
#er_res = proj_2.compute_resilience(er_data, attack_er)
#upa_res = proj_2.compute_resilience(upa_data, attack_upa)

def build_plot(res_list):
    """
    Builds a plot using a list of resiliences, returns a list of
    tuples of form (index, res_list).
    """
    output_list = []
    for res in res_list:
        output_list.append((res_list.index(res), res))
    return output_list

#network_plot = build_plot(network_res)
#er_plot = build_plot(er_res)
#upa_plot = build_plot(upa_res)

import simpleplot

#simpleplot.plot_lines("Network, ER and UPA Graphs exhibit differing resilience to random attack", 
#                      600, 600, 
#                      "N(Nodes Removed)", 
#                      "Size of Largest Connected Component", 
#                      [network_plot, er_plot, upa_plot], False, 
#                      ["Network Graph", "ER Graph with p = 0.004", "UPA Graph with m = 3"])
            
## Question 3

def fast_targeted_order(ugraph):
    """
    Takes in an undirected graph ugraph and returns a list of nodes in 
    decreasing order of their degrees.
    """    
    
    new_graph = algo.copy_graph(ugraph) #Stops us from eating our data
    
    degree_sets = []
    node_list = ugraph.keys()
    discarded = {}
    
    for poss_degree in range(len(node_list)): #O(n)
        degree_sets.append(set([]))
        discarded[poss_degree] = []
        
    for node in node_list: #O(n)
        node_deg = len(new_graph[node])
        degree_sets[node_deg].add(node)
    
    attack_list = []
        
    for poss_degree in range(len(node_list) - 1, -1, -1): #O(n)
        if len(degree_sets[poss_degree]) != 0:         
            for node in degree_sets[poss_degree]:                
                if node not in discarded[poss_degree]:
                    discarded[poss_degree].append(node)
                    for neigh in new_graph[node]:
                        neigh_deg = len(new_graph[neigh])
                        discarded[neigh_deg].append(neigh)
                        degree_sets[neigh_deg - 1].add(neigh)
                    attack_list.append(node)
                    algo.delete_node(new_graph, node)
    return attack_list
        
## Problem: Hit 587 as a neighbour first, bumping it down from the
## set to one degree below. Yet, because I iterate through the set,
## I count 587 in this set and the next. 
            
## Solution is a discard dictionary which holds things we've already gone through
## But now visiting a previous node for some reason, even if in discard dict.

## Reason was firstly, I was using a while line without decreasing the length 
## of the set. So it ran forever on the set's elements.
## Secondly, my discard dictionary was constantly re-emptying itself because 
## the corresponding entry would become [] for each non-empty set encountered.

import time

def timer(function, ugraph):
    """
    Measures how long it takes for a function to evaluate an undirected graph ugraph.
    """
    start_time = time.time()
    function(ugraph)
    end_time = time.time()
    difference = end_time - start_time
    return difference

def time_check(function):
    """
    Takes in a function and tests it on a range of upa graphs. Returns a list of tuples
    of the form (number of upa nodes, running times).
    """
    output = []
    for final_nodes in range(10, 1000, 10):
        test_graph = upa(5, final_nodes)
        time_taken = timer(function, test_graph)
        output.append((final_nodes, time_taken))
    return output

#to_time = time_check(algo.targeted_order)
#fto_time = time_check(fast_targeted_order)
#        
#simpleplot.plot_lines("CodeSkulptor Running Times of targeted_order and fast_targeted_order", 
#                      600, 600, 
#                      "N(Nodes)", 
#                      "Running Time (Seconds)", 
#                      [to_time, fto_time], False, 
#                      ["targeted_order", "fast_targeted_order"])    

## Question 4

#directed_attack_network = fast_targeted_order(network_data)
#directed_attack_er = fast_targeted_order(er_data)    
#directed_attack_upa = fast_targeted_order(upa_data)
#
#network_res2 = proj_2.compute_resilience(network_data, directed_attack_network)
#er_res2 = proj_2.compute_resilience(er_data, directed_attack_er)
#upa_res2 = proj_2.compute_resilience(upa_data, directed_attack_upa)
#
#network_plot2 = build_plot(network_res2)
#er_plot2 = build_plot(er_res2)
#upa_plot2 = build_plot(upa_res2)
#
#simpleplot.plot_lines("Network, ER and UPA Graphs exhibit differing resilience to directed attack", 
#                      600, 600, 
#                      "N(Nodes Removed)", 
#                      "Size of Largest Connected Component", 
#                      [network_plot2, er_plot2, upa_plot2], False, 
#                      ["Network Graph", "ER Graph with p = 0.004", "UPA Graph with m = 3"])

