## this is the G2o implementation, where an undirected graph is transofmed into a DAG.

import networkx as nx
import numpy as np

def g2o(input_graph,degree_threshold,step_size):

    #print(nx.info(input_graph))
    
    ### first, remove cycles
    degree_hash = input_graph.degree()
    #t1 = nx.triangles(input_graph)    
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
                input_graph.remove_edge(triplet_degrees[sorted_keys[0]],triplet_degrees[sorted_keys[1]])
            except:
                ## not all keys exist
                pass


    ## redefine hash for individual components
    #input_graph = next(nx.connected_component_subgraphs(input_graph))
    #degree_hash = input_graph.degree()
    
    outgraph = nx.DiGraph()    
    degree_list = [degree_hash[deg] for deg in degree_hash]
    threshold_degree = np.percentile(degree_list,degree_threshold)
    candidate_hotspots = [node for node,value  in degree_hash.items() if value > threshold_degree]

    print("Nodes to begin the iteration: ",len(candidate_hotspots))

    ## a queue of nodes to be processed..
    to_process = []
    
    ## a list of already processed nodes..
    already_processed = []

    ## initiate the nodes
    for node in candidate_hotspots:
        to_process.insert(0,node)
    
    while len(to_process) != 0:
        start_node = to_process.pop()
        if start_node not in already_processed:
            already_processed.append(start_node)
            for neigh in set(input_graph[start_node]):
                if neigh not in already_processed and neigh not in to_process:
                    to_process.insert(0,neigh)
                    if degree_hash[neigh] < degree_hash[start_node]:
                        outgraph.add_edge(start_node,neigh)                        
                    else:
                        outgraph.add_edge(neigh,start_node)

    print(nx.info(outgraph))
    if nx.is_directed_acyclic_graph(outgraph):
        return outgraph
    else:
        raise ValueError('Graph could not be converted to a DAG.')

def g2o_mst(input_graph):

    T = nx.minimum_spanning_tree(input_graph)
    test2 = T.to_directed()
    cycles = len(list(nx.find_cycle(test2, orientation='ignore')))
    
    return test2
    
if __name__ == '__main__':

    import rdfmodule as rm    
    import argparse
    
    parser_init = argparse.ArgumentParser()
    parser_init.add_argument("--input_graph", help="Graph in gpickle format.")
    parser_init.add_argument("--percentile", help="Degree percentile.")
    parser_init.add_argument("--jump_size", help="Neighbourhood size.")
    parser_init.add_argument("--ontology_id", help="dataset.")
    
    parsed = parser_init.parse_args()        
    G = nx.read_gpickle(parsed.input_graph)
    outgraph2 = g2o(G,parsed.percentile,parsed.jump_size)
    if parsed.ontology_id:
        rdfpart = rm.rdfconverter(outgraph2,"query")    
        rdfpart.return_target_n3("samples/"+parsed.ontology_id)
        otype = parsed.ontology_id.split(".")[1]
        rdfpart.return_background_knowledge("BK/autogen"+parsed.ontology_id,otype)
