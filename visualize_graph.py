## this python code uses in house py3plex lib for complex network visualization

import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
from py3plex.multilayer import *

def view_by_type(inputgraph,limit=False):

    input_graph = nx.read_gpickle(inputgraph)
    type_segments = defaultdict(list)
    
    for node in input_graph.nodes(data=True):
        type_segments[node[0].split("_")[0]].append(node[0])

    networks = []
    labs = []
    for k,v in type_segments.items():
        if limit != False:
            tmp_graph = input_graph.subgraph(v[0:limit]) 
        else:
            tmp_graph = input_graph.subgraph(v)
            
        if tmp_graph.number_of_edges() > 2:
            labs.append(k)
            tmp_pos=nx.spring_layout(tmp_graph)
            nx.set_node_attributes(tmp_graph,'pos',tmp_pos)
            networks.append(tmp_graph)

    print ("Visualizing..")
    draw_multilayer_default(networks,background_shape="circle",display=True,labels=labs)
    
view_by_type("./graph_datasets/biomine_dumptestgraph.gpickle")
