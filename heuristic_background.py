## this generates background knowledge..

## this file iteratively assesses heuristic speed
import networkx as nx
import numpy as np
from g2o import *
import time
import sys
import rdfmodule as rm

heuristics = ["degree","pagerank_scipy","eigenvector","communicability","closeness","betweenness"]
input_graphs = ["graph_datasets/snpsstep1.gpickle"]

results = []

for h in heuristics:
    for inp in input_graphs:
        print("dataset: ",inp, " and heuristic: ",h)
        start = time.time()
        G = nx.read_gpickle(inp)
        res_graph = g2o(G,95,1,h)
        rdfpart = rm.rdfconverter(res_graph,"query")
        rdfpart.return_background_knowledge("BK/knowledge_"+h+".n3","n3")
