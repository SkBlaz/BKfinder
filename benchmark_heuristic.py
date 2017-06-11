## this file iteratively assesses heuristic speed
import networkx as nx
import numpy as np
from g2o import *
import time
import sys

heuristics = ["degree","pagerank_scipy","eigenvector","communicability","closeness","betweenness"]
input_graphs = ["graph_datasets/snps.gpickle","graph_datasets/biominetestgraph.gpickle"]

results = []
for j in range(0,10,1):
    for h in heuristics:
        for inp in input_graphs:
            print("dataset: ",inp, " and heuristic: ",h)
            start = time.time()
            G = nx.read_gpickle(inp)
            res_graph = g2o(G,90,1,h)
            finaltime = time.time()-start
            n_nodes = len(res_graph.nodes())
            n_edges = len(res_graph.edges())
            results.append((inp,h,n_nodes,n_edges,finaltime))

import json
with open(sys.argv[1], 'w') as outfile:
    json.dump(results, outfile)
