## this is the G2o implementation, where an undirected graph is transofmed into a DAG.

import networkx as nx
import numpy as np

def g2o(input_graph,degree_threshold,step_size,heuristic="degree"):

    ## heuristic selection
    if heuristic == "degree":
        heuristic_hash = input_graph.degree()
    elif heuristic == "pagerank":
        heuristic_hash = nx.pagerank_numpy(input_graph, alpha=0.9)
    elif heuristic == "pagerank_scipy":
        heuristic_hash = nx.pagerank_scipy(input_graph, alpha=0.9)
    elif heuristic == "eigenvector":
        heuristic_hash = nx.eigenvector_centrality_numpy(input_graph)
    elif heuristic == "communicability":
        heuristic_hash = nx.communicability_centrality(input_graph)
    elif heuristic == "flow_betweenness":
        heuristic_hash = nx.current_flow_betweenness_centrality(input_graph)
    elif heuristic == "closeness":
        heuristic_hash = nx.closeness_centrality(input_graph)
    elif heuristic == "betweenness":
        heuristic_hash = nx.betweenness_centrality(input_graph)
    else:        
        raise ValueError("Please select a valid heuristic..")

    ## first identify the triplets
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
                result_triplets.append( (node,neigh,both))

    ## remove triplets in some manner
    for triplet in result_triplets:
        
        ## get the node degrees
        triplet_degrees = {heuristic_hash[node] : node for node in triplet}
        sorted_keys = sorted(list(triplet_degrees.keys()))
        if len(sorted_keys) == 3:
            try:            
                input_graph.remove_edge(triplet_degrees[sorted_keys[0]],triplet_degrees[sorted_keys[1]])
            except:
                ## not all keys exist
                pass

    
    outgraph = nx.DiGraph()    
    degree_list = [heuristic_hash[deg] for deg in heuristic_hash]
    threshold_degree = np.percentile(degree_list,degree_threshold)
    candidate_hotspots = [node for node,value  in heuristic_hash.items() if value > threshold_degree]

    print("Nodes to begin the iteration: ",len(candidate_hotspots))

    ## a queue of nodes to be processed..
    to_process = []
    
    ## a list of already processed nodes..
    already_processed = []

    ## initiate the nodes
    for node in candidate_hotspots:
        to_process.insert(0,node)
    
    while len(to_process) != 0:
        for step in (range(0,int(step_size))):
            ## go to a specific depth
            if len(to_process) != 0:
                start_node = to_process.pop()
            else:
                break
            if start_node not in already_processed:
                already_processed.append(start_node)
                for neigh in set(input_graph[start_node]):
                    if neigh not in already_processed and neigh not in candidate_hotspots:
                        ## Querying
                        if step > 0:
                            to_process.append(neigh)
                        else:
                            to_process.insert(0,neigh)
                        ## Edge construction step    
                        if heuristic_hash[neigh] < heuristic_hash[start_node]:
                            outgraph.add_edge(start_node,neigh)
                        else:
                            outgraph.add_edge(neigh,start_node)

    print(nx.info(outgraph))
    if nx.is_directed_acyclic_graph(outgraph):
        return outgraph
    else:
        raise ValueError('Graph could not be converted to a DAG.')
    
if __name__ == '__main__':

    import rdfmodule as rm    
    import argparse
    
    parser_init = argparse.ArgumentParser()
    parser_init.add_argument("--input_graph", help="Graph in gpickle format.")
    parser_init.add_argument("--percentile", help="Degree percentile.")
    parser_init.add_argument("--step_size", help="Neighbourhood size.")
    parser_init.add_argument("--heuristic", help="possible options: degree, pagerank_numpy, pagerank_scipy, katz, eigenvector_centrality_numpy, flow_betweenness, communicability, pagerank_scipy")
    parser_init.add_argument("--ontology_id", help="dataset.")
    parser_init.add_argument("--make_samples", help="dataset.")
    parser_init.add_argument("--output_graph", help="dataset.")
    
    parsed = parser_init.parse_args()        
    G = nx.read_gpickle(parsed.input_graph)

    if parsed.output_graph:
        nx.write_gpickle(result_graph, "graph_datasets/"+job_id+".gpickle")
    outgraph2 = g2o(G,parsed.percentile,parsed.step_size,parsed.heuristic)

    if parsed.ontology_id:
        rdfpart = rm.rdfconverter(outgraph2,"query") ## query is the folder with lists
        if parsed.make_samples:
            rdfpart.return_target_n3("samples/"+parsed.ontology_id) ## target folder
        otype = parsed.ontology_id.split(".")[1]
        rdfpart.return_background_knowledge("BK/autogen"+parsed.ontology_id,otype)
