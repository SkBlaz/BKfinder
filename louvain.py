import networkx as nx
import community
import matplotlib.pyplot as plt

#G = nx.random_graphs.powerlaw_cluster_graph(10000, 1, .4)
#G = nx.newman_watts_strogatz_graph(1000, 15, 0.02, seed=None)
G = nx.barabasi_albert_graph(10000, 1, seed=None)
Gx = nx.Graph()
#G = nx.read_gpickle("graph_datasets/snpsstep1.gpickle")

nodes = G.nodes(data=False)
edges = G.edges(data=False)

Gx.add_nodes_from(nodes)
Gx.add_edges_from(edges)

part = community.best_partition(Gx)
values = [part.get(node) for node in G.nodes()]

nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)

#nx.draw_spring(Gx,node_color="black")

plt.show()
