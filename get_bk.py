## This is some basic code used to obtain the data from the Biomine API
## and transform it into a graph, which will be further on processed.

import urllib.request
import urllib.parse
import json
import urllib
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class make_request:

    def __init__(self):

        self.db_url =  'http://biomine.ijs.si/list_databases'
        self.bm_api = 'http://biomine.ijs.si/api'
        self.databases = json.loads(urllib.request.urlopen(self.db_url).read().decode())['databases']

    def get_info(self):

        print ('databases:{}  API:{}'.format(self.db_url,self.bm_api))

    def list_db(self):

        print (self.databases)

    def test_query(self):
        
        ##additional source and target nodes can be added.

        #params2 = urllib.parse.urlencode({'sourceTerms': 'InterPro:IPR011364, EntrezGene:672','graph_type': 'json'}).encode('utf-8')

        params = urllib.parse.urlencode({'database': self.databases['biomine'][0],
                                    'sourceTerms': 'EntrezGene:27086',
                                    'targetTerms': 'EntrezGene:93986',
                                    'maxnodes': 500,
                                    'grouping': 5,
                                          'graph_type': 'json'}).encode("utf-8")


        json_graph =  json.loads(urllib.request.urlopen(self.bm_api, params).read().decode())['graph']
        
        ## save for possible further use..
        print ("Data obtained, constructing the graph..")
        nodes = json.loads(json_graph)['nodes']
        edges = json.loads(json_graph)['links']
        ## colors

        ## lets create a graph..

        G = nx.Graph()

        ## those are the names..
        labels = {}
        for id,node in enumerate(nodes):
            #print (id, node['id'])
            G.add_node(id)
            labels[id] = node['id']
        for id,edge in enumerate(edges):
            #print (id, edge['source'],edge['target'])
            G.add_edge(int(edge['source']),int(edge['target']))
            
        
        print ("Finished")
        pos = nx.spring_layout(G)
        nx.draw(G,pos)
        nx.draw_networkx_labels(G,pos,labels,font_size=16)
        plt.show()

        return G
        
    def execute_query(self,sourceterms,targetterms=None, maxnodes=200,grouping=0):
        
        
        print ("Search executed..")
        
        ## decide on search type

        if targetterms == None:
            params = urllib.parse.urlencode({'database': self.databases['biomine'][0],
                                             'sourceTerms': sourceterms,
                                             'maxnodes': maxnodes,
                                             'grouping': grouping,
                                             'graph_type': 'json'}).encode("utf-8")
        else:
            params = urllib.parse.urlencode({'database': self.databases['biomine'][0],
                                             'sourceTerms': sourceterms,
                                             'targetTerms': targetterms,
                                             'maxnodes': maxnodes,
                                             'grouping': grouping,
                                             'graph_type': 'json'}).encode("utf-8")

        
        json_graph =  json.loads(urllib.request.urlopen(self.bm_api, params).read().decode())['graph']
        
        ## save for possible further use..
        print ("Data obtained, constructing the graph..")
        nodes = json.loads(json_graph)['nodes']
        edges = json.loads(json_graph)['links']
        ## colors

        ## lets create a graph..

        G = nx.Graph()

        ## those are the names..
        labels1 = {}

        for id,node in enumerate(nodes):

            if node['organism'] == 'hsa':

                G.add_node(id, name=node['id'], degree=node['degree'], spec=node['organism'], color = 'r')

            else:
                G.add_node(id, name=node['id'], degree=node['degree'], spec=node['organism'], color = 'g')

            labels1[id] = node['id']

        for id,edge in enumerate(edges):

            G.add_edge(int(edge['source']),int(edge['target']), weight = edge['reliability'])
                    
        ## color according to db entry at least.

        edgesG = G.edges()
        nodesG = G.nodes(data=True)
        
        ## assign values to the object for further use

        self.graph_node_degree = [int(u[1]['degree']) for u in nodesG]
        self.graph_node_colors = [u[1]['color'] for u in nodesG]
        self.graph_weights = [G[u][v]['weight'] for u,v in edgesG]
        self.graph = G        
        self.labels = labels1
        self.pos = nx.spring_layout(G)
        #self.pos = nx.circular_layout(G)
        return G

    def draw_graph(self, labs = False, weights = True, fsize = 10):
        
        nsize = [deg*0.1 for deg in self.graph_node_degree]

        if weights == False:
            if labs == True:
                nx.draw(self.graph,self.pos,node_size=nsize, node_color = self.graph_node_colors)
                nx.draw_networkx_labels(self.graph,self.pos,self.labels,font_size=16)
                plt.show()
            else:
                nx.draw(self.graph,self.pos,node_size=nsize,node_color = self.graph_node_colors)
                nx.draw_networkx_labels(self.graph,self.pos,font_size=16)
                plt.show()
        else:
            if labs == True:
                nx.draw(self.graph,self.pos, width=self.graph_weights,node_size=nsize,node_color = self.graph_node_colors)
                nx.draw_networkx_labels(self.graph,self.pos,self.labels,font_size=fsize)
                plt.show()
            else:
                nx.draw(self.graph,self.pos, width=self.graph_weights,node_size=nsize,node_color = self.graph_node_colors)
                nx.draw_networkx_labels(self.graph,self.pos,font_size=fsize)
                plt.show() 

def read_example_data(max):

    outlist = []
    outlist2 = []

    with open("data/cancer.list") as cl:
        for line in cl:
           outlist.append("UniProt:"+line.replace("\n",""))

    with open("data/alzheimer.list") as cl:
        for line in cl:
           outlist2.append("UniProt:"+line.replace("\n",""))

    return (",".join(outlist[1:max]),",".join(outlist2))


if __name__ == '__main__':
    
    source, target = read_example_data(200)

    ## init a request
    request = make_request()
    
    ## this returns graph for further reduction use..
    request.execute_query(source)
    request.draw_graph()

