## This is some basic code used to obtain the data from the Biomine API
#from joblib import Parallel, delayed
#import multiprocessing## and transform it into a graph, which will be further on processed.

import argparse
import matplotlib.pyplot as plt
import urllib.request
import urllib.parse
import json
import urllib
import networkx as nx
import numpy as np
import rdfmodule as rm
import sys
import os



class make_request:

    def __init__(self):

        self.db_url =  'http://biomine.ijs.si/list_databases'
        self.bm_api = 'http://biomine.ijs.si/api'
        self.databases = json.loads(urllib.request.urlopen(self.db_url).read().decode())['databases']
        self.graph = nx.Graph()
        self.graph_nodes = []
        
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
    
    def execute_query_orto(self,sourceterms,targetterms=None, maxnodes=2000,grouping=0,omit='hsa'):
        
        
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

        #Go = nx.Graph()

        
        ## those are the names..
        
        labels1 = {}

        for id,node in enumerate(nodes):


            if node['organism'] != omit:

                G.add_node(id, name=node['id'], degree=node['degree'], spec=node['organism'], color = 'b')

                labels1[id] = node['id']

        for id,edge in enumerate(edges):
            if edge['source'] in G.nodes() and edge['target'] in G.nodes():
                G.add_edge(int(edge['source']),int(edge['target']), weight = edge['reliability'])

            if node['organism'] == omit:

                G.add_node(id, name=node['id'], degree=node['degree'], spec=node['organism'], color = 'r')

                labels1[id] = node['id']

        for id,edge in enumerate(edges):
            
            if edge['source'] in G.nodes() and edge['target'] in G.nodes():
            
                G.add_edge(int(edge['source']),int(edge['target']), weight = edge['reliability'])
            #Go.add_edge(int(edge['source']),int(edge['target']), weight = edge['reliability'])

                    
        ## color according to db entry at least.

        edgesG = G.edges()
        nodesG = G.nodes(data=True)

        

        # ## assign values to the object for further use
        self.graph_node_degree_ortolog = [int(u[1]['degree']) for u in nodesG]
        self.graph_node_colors_ortolog = [u[1]['color'] for u in nodesG]
        self.graph_weights_ortolog = [G[u][v]['weight'] for u,v in edgesG]
        self.graph_ortolog = G        
        self.labels_ortolog = labels1
        self.pos_ortolog = nx.spring_layout(G)




        ## assign values to the object for further use

        self.graph_node_degree_ortolog = [int(u[1]['degree']) for u in nodesG]
        self.graph_node_colors_ortolog = [u[1]['color'] for u in nodesG]
        self.graph_weights_ortolog = [G[u][v]['weight'] for u,v in edgesG]
        self.graph_ortolog = G        
        self.labels_ortolog = labels1
        self.pos_ortolog = nx.spring_layout(G)
        self.pos = nx.circular_layout(G)

        return G
    
    def execute_query(self,sourceterms,targetterms=None, maxnodes=2000,grouping=0):
        
        
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
        #Go = nx.Graph()
        
        ## those are the names..
        
        labels1 = {}

        for id,node in enumerate(nodes):

            if node['organism'] == 'hsa':

                G.add_node(id, name=node['id'], degree=node['degree'], spec=node['organism'], color = 'r')

            else:

                #Go.add_node(id, name=node['id'], degree=node['degree'], spec=node['organism'], color = 'g')
                
                G.add_node(id, name=node['id'], degree=node['degree'], spec=node['organism'], color = 'g')

            labels1[id] = node['id']

        for id,edge in enumerate(edges):

            G.add_edge(int(edge['source']),int(edge['target']), weight = edge['reliability'])
            #Go.add_edge(int(edge['source']),int(edge['target']), weight = edge['reliability'])
                    
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
        print (nx.info(G))

    def execute_query_inc(self,sourceterms,targetterms=None, maxnodes=2000,grouping=0, div=4,connected=False):

        max_terms = len(sourceterms)
        ## init the graph structure..

        G = self.graph

        step = div

#        step = int(len(sourceterms)/div)

        if step > 1500:
            step = 1000
        # to make it run in parallel, simply divide sourceterms by step before this loop
        
        print ("Initiating the graph construction phase with step: ",str(step))

        tmplist = []
        iteration = 0
        
        for e,k in enumerate(sourceterms):

            tmplist.append(k)
            
            if e % step == 0 and e > 0:

                sterms = ",".join(tmplist)

                tmplist = []                
                try:
                    if targetterms == None:
                    
                        params = urllib.parse.urlencode({'database': self.databases['biomine'][0],
                                'sourceTerms': sterms,
                                'maxnodes': maxnodes,
                                'grouping': grouping,
                                'graph_type': 'json'}).encode("utf-8")
                    
                        json_graph =  json.loads(urllib.request.urlopen(self.bm_api, params).read().decode())['graph']
                except:
                    print ("passing")
                    pass
        
                ## save for possible further use..
                print ("Progress: ",str(round(float(e/max_terms)*100,2)),"% complete.", nx.info(self.graph))

                iteration += 1

                nodes = json.loads(json_graph)['nodes']
                edges = json.loads(json_graph)['links']                
                node_hash = {}

                for id,node in enumerate(nodes):

                    col_value = "r"
                    
                    try:

                        if node['organism'] == 'hsa':

                            col_value = "r"
                        
                        elif node['organism'] == 'mmu':
                        
                            col_value = "g"
                            
                        else:

                            col_value = "y"
                            
                    except:
                        pass
                        
                    node_hash[id] = (node['id'], node['degree'],col_value)
                    if iteration == 1:
                        self.graph_nodes.append(node['id'])
                    
                for edge in edges:

#                    print (edge['source'],node_hash[int(edge['source'])])
                    sourceterms = node_hash[int(edge['source'])]
                    targets = node_hash[int(edge['target'])]
                    if connected == False:
                        
                        G.add_node(sourceterms[0],degree=sourceterms[1],color=sourceterms[2])
                        G.add_node(targets[0],degree=targets[1],color=targets[2])
                        G.add_edge(sourceterms[0],targets[0],weight=edge['reliability'], key=edge['key'])
                        
                    else:
                        if targets[0] in self.graph_nodes or sourceterms[0] in self.graph_nodes:

                            if targets[0] not in self.graph_nodes:
                                self.graph_nodes.append(targets[0])
                            if sourceterms[0] not in self.graph_nodes:
                                self.graph_nodes.append(sourceterms[0])
                            
                            G.add_node(sourceterms[0],degree=sourceterms[1],color=sourceterms[2])
                            G.add_node(targets[0],degree=targets[1],color=targets[2])
                            G.add_edge(sourceterms[0],targets[0],weight=edge['reliability'], key=edge['key'])


        ## color according to db entry at least.
           
        edgesG = G.edges()
        nodesG = G.nodes(data=True)
        print ("Final size: \n",nx.info(G))

        ## assign values to the object for further use
        
        self.graph_node_degree = [int(u[1]['degree']) for u in nodesG]
        self.graph_node_colors = [u[1]['color'] for u in nodesG]
        self.graph_weights = [G[u][v]['weight'] for u,v in edgesG]
        self.graph = G        
        self.pos = nx.spring_layout(G)
        return G

    def reset_graph(self):

        self.graph = nx.Graph()
        
    def get_graph(self):

        return self.graph
    
    
    def trim_graph(self, degreetrim):

        print ("Trimming the graph..")
        to_remove = [n if self.graph.degree(n) < degreetrim else None  for n in self.graph.nodes()]
        self.graph.remove_nodes_from(to_remove)

    def draw_graph(self, labs = False, weights = True, fsize = 10):

        nsize = [deg*0.1 for deg in self.graph_node_degree]

        if weights == False:

            if labs == True:

                nx.draw(self.graph,self.pos,node_size=nsize, node_color = self.graph_node_colors)
                nx.draw_networkx_labels(self.graph,self.pos,self.labels,font_size=16)
                plt.show()
            else:
                nx.draw(self.graph,self.pos,node_size=nsize,node_color = self.graph_node_colors)
                #nx.draw_networkx_labels(self.graph,self.pos,font_size=16)
                plt.show()
        else:
            if labs == True:
                nx.draw(self.graph,self.pos, width=self.graph_weights,node_size=nsize,node_color = self.graph_node_colors)
                nx.draw_networkx_labels(self.graph,self.pos,self.labels,font_size=fsize)
                plt.show()
            else:
                nx.draw(self.graph,self.pos, width=self.graph_weights,node_size=nsize,node_color = self.graph_node_colors)
                #nx.draw_networkx_labels(self.graph,self.pos,font_size=fsize)
                plt.show()

    def draw_graph_ortolog(self, labs = False, weights = True, fsize = 10):
        import matplotlib.pyplot as plt
        nsize = [deg*0.1 for deg in self.graph_node_degree_ortolog]

        if weights == False:

            if labs == True:

                nx.draw(self.graph_ortolog,self.pos,node_size_ortolog=nsize, node_color = self.graph_node_colors_ortolog)
                nx.draw_networkx_labels(self.graph_ortolog,self.pos_ortolog,self.labels_ortolog,font_size=16)
                plt.show()
            else:
                nx.draw(self.graph_ortolog,self.pos_ortolog,node_size=nsize,node_color = self.graph_node_colors_ortolog)
                nx.draw_networkx_labels(self.graph_ortolog,self.pos_ortolog,font_size=16)
                plt.show()
        else:
            if labs == True:

                nx.draw(self.graph_ortolog,self.pos_ortolog, width=self.graph_weights_ortolog,node_size=nsize,node_color = self.graph_node_colors_ortolog)
                nx.draw_networkx_labels(self.graph_ortolog,self.pos_ortolog,self.labels_ortolog,font_size=fsize)
                plt.show()
            else:
                nx.draw(self.graph_ortolog,self.pos_ortolog, width=self.graph_weights_ortolog,node_size=nsize,node_color = self.graph_node_colors_ortolog)
                nx.draw_networkx_labels(self.graph_ortolog,self.pos_ortolog,font_size=fsize)
                plt.show() 

    def export_graph(self,gname):

        nx.write_gml(G, gname+".gml")
        
        return
        
# def read_example_data(max):

#     outlist = []
#     outlist2 = []

#     with open("data/cancer.list") as cl:
#         for line in cl:
#            outlist.append("UniProt:"+line.replace("\n",""))

#     with open("data/alzheimer.list") as cl:
#         for line in cl:
#            outlist2.append("UniProt:"+line.replace("\n",""))

#     return (",".join(outlist[1:max]),",".join(outlist2[1:max]))

def read_example_datalist(whole=False):

    outlist = []
    outlist2 = []
    filenames = ["./data/"+f for f in os.listdir("data")]
    for f in filenames:
        print ("Adding: "+f)
        with open(f) as cl:
            for line in cl:
                outlist.append("UniProt:"+line.replace("\n",""))

    return (outlist,outlist2)        


if __name__ == '__main__':

    parser_init = argparse.ArgumentParser()
    
    parser_init.add_argument("--step_size", help="How large subgraphs are taken when building main graph")
    parser_init.add_argument("--output_name", help="Custom job ID for saving graph")
    parser_init.add_argument("--visualize", help="Basic network visualization with networkx module")
    parser_init.add_argument("--ontology_output", help="Ontology mapping generation")
    parser_init.add_argument("--py3plex", help="Multiplex network visualization")
    parser_init.add_argument("--instructions", help="Load the bio identifier lists in separate files into data folder and run this tool at least with --step_size option")

    parser = parser_init.parse_args()
    
    source, target = read_example_datalist(whole=True)

    source = source
    
    ## init a request
    
    request = make_request()
    
    ## this returns graph for further reduction use..
    
    if(parser.step_size):

        result_graph = request.execute_query_inc(source,div=int(parser.step_size),connected=False)

        if (parser.output_name):
            job_id = parser.output_name
            print ("Writing pickle datadump..")
            nx.write_gpickle(result_graph, "graph_datasets/biomine_dump"+job_id+".gpickle")

            if (parser.ontology_output):
                rdfpart = rm.rdfconverter(result_graph,"data")
                rdfpart.return_target_n3("samples/dataset"+job_id+".n3")
                rdfpart.return_background_knowledge("BK/autogen"+job_id+".n3")

        if (parser.visualize): 
            request.draw_graph(labs=False)


