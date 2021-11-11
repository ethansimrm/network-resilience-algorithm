### Project 2: Connected Components and Graph Resilience
"""
This document contains the functions required for
Algorithmic Thinking 1 Module 2 Project and Application.
"""

## Implement BFS algorithm

import poc_queue as provided

GRAPH0 = {0: set([1]),
          1: set([0, 2]),
          2: set([1, 3]),
          3: set([2])}

GRAPH1 = {0: set([1]),
          1: set([0]),
          2: set([]),
          3: set([])}

def bfs_visited(ugraph, start_node):
    """
    For an undirected graph ugraph, return set of all
    nodes visited when start_node is the first node 
    considered.
    """
    bfs_q = provided.Queue()
    visited = set([start_node])
    bfs_q.enqueue(start_node)
    while len(bfs_q) != 0:
        considered = bfs_q.dequeue()
        for neighbor in ugraph[considered]:
            if neighbor not in visited:
                visited.add(neighbor)
                bfs_q.enqueue(neighbor)
    return visited

#print bfs_visited(GRAPH0, 0)
        
## Connected components

def cc_visited(ugraph):
    """
    Takes an undirected graph ugraph and returns a list
    of sets. Each set is one distinct connected component.
    """
    keys = ugraph.keys()
    remaining_nodes = set(keys)
    conn_comp = []
    for node in keys:
        if node in remaining_nodes:
            component = bfs_visited(ugraph, node)
            conn_comp.append(component)
            for node in component:
                remaining_nodes.discard(node)
    return conn_comp

#print cc_visited(GRAPH1)
    
def largest_cc_size(ugraph):
    """
    Takes an undirected graph ugraph and returns an integer
    corresponding to the size of the largest connected
    component.
    """
    cc_list = cc_visited(ugraph)
    biggest_cc = 0
    for conn_comp in cc_list:
        if len(conn_comp) > biggest_cc:
            biggest_cc = len(conn_comp)
    return biggest_cc

#print largest_cc_size(GRAPH1)

def compute_resilience(ugraph, attack_order):
    """
    Takes undirected graph ugraph, list of nodes
    attack_order, and iterates through the latter.
    For each node in the list, it is removed, and largest
    connected component size computed for each removal.
    
    Returns a list where the first item is largest cc size
    for untouched graph, and then next item is largest cc
    size following one removal, and so on.
    """
    res_track = [largest_cc_size(ugraph)]
    for node in attack_order:
        down_conn = ugraph.pop(node)
        for neighbor in down_conn:
            ugraph[neighbor].discard(node)
        res_track.append(largest_cc_size(ugraph))
    return res_track

#print compute_resilience(GRAPH1, [2])
            
