# network-resilience-algorithm

This is my solution to another graph theory problem - this time focusing on computer networks - formulated as part of the Algorithmic Thinking course, organised by Rice University's Department of Computer Science.

Here, I implement the BFS and CC algorithms, and use them to determine the largest connected component of a graph. I also create a function (compute_resilience) to simulate an "attack" on this graph, by removing nodes and then calculating the size of the largest remaining connected component.

My work thus far is mirrored in bfs_cc_implement_mirror.py, and due to the highly specific nature of the modules imported, can only run in CodeSkulptor (a browser-based IDE also created by the Rice University Department of Computer Science) - you can access it at https://py2.codeskulptor.org/#user48_E90mZSM3mM_16.py.

I then create random undirected graphs generated by implementing algorithm ER and undirected graphs (rich-gets-richer) generated by a modified implementation of algorithm DPA, and implement the algorithm Fast_Targeted_Order to compute an attack list - a list of nodes ordered by degree in descending order. I then apply this algorithm (and a random attack list) to the ER and UPA graphs, and calculate their resiliences under attack. I also do the same to a graphical representation of a computer network. We find that the computer network is not resilient under this type of targeted attack, while the ER graph is (the UPA graph is a borderline case). 

This second portion is mirrored in nr_tester_mirror.py, and again, due to the highly specific nature of the modules imported, can only run in CodeSkulptor. It can be accessed at https://py2.codeskulptor.org/#user48_bBaHm3VHv2_121.py. 
