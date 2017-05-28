## this is the G2o implementation, where an undirected graph is transofmed into a DAG.



import networkx as nx
import numpy as np


def g2o(input_graph,degree_threshold,step_size):

 #   print(nx.info(input_graph))
    
    ### first, remove cycles
    degree_hash = input_graph.degree()
    t1 = nx.triangles(input_graph)    
    G=input_graph
    result_triplets=[]
    crossed=set()    
    for node in G:
        crossed.add(node)    
        done_count=set()    
        neighbours=set(G[node])
        for neigh in neighbours:
            if neigh in crossed:    
                continue    
            done_count.add(neigh)    
            for both in neighbours.intersection(G[neigh]):
                if both in crossed or both in done_count:    
                    continue    
                result_triplets.append( (node,neigh,both) )

    for triplet in result_triplets:
        
        ## get the node degrees
        triplet_degrees = {degree_hash[node] : node for node in triplet}
        sorted_keys = sorted(list(triplet_degrees.keys()))
        if len(sorted_keys) == 3:
            try:                
                input_graph.remove_node(triplet_degrees[sorted_keys[0]]) 
            except:                
                ##node already deleted..
                pass

    ## definitions for the second part of the process
    
    outgraph = nx.DiGraph()    
    degree_list = [degree_hash[deg] for deg in degree_hash]
    threshold_degree = np.percentile(degree_list,degree_threshold)
    candidate_hotspots = [node for node,value  in degree_hash.items() if value > threshold_degree]

    print("Nodes to begin the iteration: ",len(candidate_hotspots))

    ## those are the initial conditions
    
    to_process = []
    already_processed = []
    
    for node in candidate_hotspots:
        to_process.insert(0,node)

    while len(to_process) != 0:

        ## do some stuff here..
        
        pass
        ## pop an item from the back
        ## construct node with diedges to depth of step
        ## if diedge partner not yet in checked
        ## put neighbours into the seen list
        ## repeat
        
    
#    print(nx.info(input_graph))    
#    print(nx.is_directed_acyclic_graph(input_graph))

G = nx.read_gpickle("graph_datasets/biomine_dumptestgraph.gpickle")
g2o(G,95,1)
