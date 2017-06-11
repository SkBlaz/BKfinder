### this is the algortihm capable of clustering

import networkx as nx
import numpy as np
import argparse
from sklearn.cluster import KMeans
from collections import defaultdict

def graph_cluster(input_graph,tlist,cl_num):

    outdict = defaultdict(list)
    graph_nodes = input_graph.nodes()
    distance_matrix = nx.floyd_warshall_numpy(input_graph,nodelist=tlist,weight='reliability')

    distance_matrix[distance_matrix == np.inf] = len(graph_nodes)
    print("Clustering part..")    
    clustering_algorithm = KMeans(n_clusters=int(cl_num), max_iter=600).fit(distance_matrix)
    predictions = clustering_algorithm.predict(distance_matrix)
    for gn, pred in  zip(graph_nodes,predictions):
        outdict[pred].append(gn)
    
    
    return outdict
    

if __name__ == '__main__':

    parser_init = argparse.ArgumentParser()
    parser_init.add_argument("--input_graph", help="Graph in gpickle format.")
    parser_init.add_argument("--input_nodelist", help="Nodelist input..")
    parser_init.add_argument("--number_clusters", help="Cluster_number..")
    parser_init.add_argument("--output_folder", help="prediction_file..")
    
    parsed = parser_init.parse_args()        
    G = nx.read_gpickle(parsed.input_graph)
    termlist = []

    with open(parsed.input_nodelist) as nl:
        for line in nl:
            parts = line.strip().split()
            termlist.append(parts[0])
            
    predictions = graph_cluster(G,termlist,parsed.number_clusters)

    for k,v in predictions.items():
        f = open(str(parsed.output_folder)+"/"+str(k)+"cluster", 'w')
        outdata = "\n".join([x.split(":")[1] for x in v])
        f.write(outdata)
        f.close()
