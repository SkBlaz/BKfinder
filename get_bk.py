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
        

        


    ## convert it to some sort of networkx structure..

if __name__ == '__main__':

    ## init a request
    request = make_request()

    ## some tests
    #request.get_info()
    #request.list_db()
    print(request.test_query())
