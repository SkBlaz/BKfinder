## this file iteratively assesses heuristic speed
import networkx as nx
import numpy as np
from g2o import *

heuristics = ["degree","pagerank_scipy","eigenvector","communicability","closeness","betweenness"]
input_graphs = ["graph_datasets/snps.gpickle","graph_datasets/biominetestgraph.gpickle"]

results = []
for h in heuristics:
    for inp in input_graphs:
        print("dataset: ",inp, " and heuristic: ",h)
        G = nx.read_gpickle(inp)
        res_graph = g2o(G,90,1,h)
        n_nodes = len(res_graph.nodes())
        n_edges = len(res_graph.edges())
        results.append((inp,h,n_nodes,n_edges))

import json
with open('OUTPUT/speed.json', 'w') as outfile:
    json.dump(results, outfile)
