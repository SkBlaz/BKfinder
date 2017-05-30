## this is the RDF to NetworkX converter class..

import rdflib
import sys
from collections import defaultdict
import os
import networkx as nx
from random import randint


class rdfconverter:
    
    def __init__(self, nxgraph, classfolder):
        
        self.nxgraph = nxgraph
        self.cfile = classfolder


    def test(self):
        print ("Class called OK.")

    def return_BK(self,outfile):
        g = rdflib.graph.Graph()
        KT = rdflib.Namespace('http://kt.ijs.si/hedwig#')
        amp_uri = 'http://kt.ijs.si/ontology/hedwig#'
        obo_uri = "http://purl.obolibrary.org/obo/"
        AMP = rdflib.Namespace(amp_uri)        
        ontology = defaultdict(list)
        for node in self.nxgraph.nodes():
            for node2 in self.nxgraph[node]:
                ontology[ str(node).split(":")[1] ].append( str(node2).split(":")[1])
        print (ontology)
        
    def return_background_knowledge(self, outfile,ontology_type):        
        
        ## construct the background knowledge..
        
        g = rdflib.graph.Graph()
        KT = rdflib.Namespace('http://kt.ijs.si/hedwig#')
        amp_uri = 'http://kt.ijs.si/ontology/hedwig#'
        obo_uri = "http://purl.obolibrary.org/obo/"
        AMP = rdflib.Namespace(amp_uri)        
        ontology = defaultdict(list)

        for edge in self.nxgraph.edges():
            u = rdflib.term.URIRef('%s%s' % (obo_uri, edge[0]))
            annotation_uri = rdflib.term.URIRef('%s%s' % (obo_uri, rdflib.Literal(edge[1])))
            g.add((annotation_uri, rdflib.RDFS.subClassOf,u))
            
#        terms = dict(nx.get_node_attributes(self.nxgraph, 'name'))


        # for node in self.nxgraph.nodes():
            
        #     for node2 in self.nxgraph.neighbors(node):
        #         ontology[ str(node).split(":")[1] ].append( str(node2).split(":")[1])
                
        # for id, example1 in enumerate(ontology.keys()):

        #     # Write to rdf graph                         

        #     u = rdflib.term.URIRef('%sTERM%s' % (obo_uri, example1))

        #     #g.add((u, rdflib.RDF.type, KT.is_a))

        #     for ex in ontology[example1]:
        #         annotation_uri = rdflib.term.URIRef('%s%s' % (obo_uri, rdflib.Literal(ex)))
        #         g.add((annotation_uri, rdflib.RDFS.subClassOf,u))

        self.rdfgraph = g

        g.serialize(destination=outfile,format=ontology_type)

        print ("BK constructed.")
        return 0
        
    def return_target_n3(self, outfile,random=False):

        print ("Transforming the data..")
        target_dict = defaultdict(list)
        filenames = [self.cfile+"/"+f for f in os.listdir(self.cfile)]
        for file in filenames:
            with open(file) as f:
                for ind,line in enumerate(f):
                    target_dict[file].append( line.replace("\n","") )                        

        ## generate query sample sets
        
        ## construct target class ontology
        g = rdflib.graph.Graph()
        KT = rdflib.Namespace('http://kt.ijs.si/hedwig#')
        amp_uri = 'http://kt.ijs.si/ontology/hedwig#'
        obo_uri = "http://purl.obolibrary.org/obo/"
        AMP = rdflib.Namespace(amp_uri)
        
        for id, example1 in enumerate(target_dict.keys()):
            
            # Write to rdf graph
            print("Processing: ",example1)
        
            u = rdflib.term.URIRef('%sexample%s' % (amp_uri, id))
            g.add((u, rdflib.RDF.type, KT.Example))
            g.add((u, KT.class_label, rdflib.Literal(example1)))
                        
            for ex in target_dict[example1]:
                  
                annotation_uri = rdflib.term.URIRef('%s%s' % (obo_uri, rdflib.Literal(ex)))
                blank = rdflib.BNode()
                g.add((u, KT.annotated_with, blank))
                g.add((blank, KT.annotation, annotation_uri))
            
        g.serialize(destination=outfile,format='n3')
        print ("Data transformed.")
        return 0
    
    def return_target_n3_detailed(self, outfile):

        ## this function takes individual edges and annotates them according to the key property!
        ## this is a more detailed annotation, which can be further used for BK construction!
        pass
    def rdf_get_graph(self):
        ## check if rdf graph is valid one
        return self.rdfgraph
    
