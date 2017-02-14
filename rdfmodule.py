## this is the RDF to NetworkX converter class..

import rdflib
import sys
from collections import defaultdict
import os
import networkx as nx
class rdfconverter:
    
    def __init__(self, nxgraph, classfolder):
        
        self.nxgraph = nxgraph
        self.cfile = classfolder

    def test(self):
        print ("Class called OK.")
        
    def return_background_knowledge(self, outfile):        

        targetdict = self.return_target_n3()
        
        ## construct the background knowledge..
        
        g = rdflib.graph.Graph()
        KT = rdflib.Namespace('http://kt.ijs.si/hedwig#')
        amp_uri = 'http://kt.ijs.si/ontology/hedwig#'
        obo_uri = "http://purl.obolibrary.org/obo/"
        AMP = rdflib.Namespace(amp_uri)        
        ontology = defaultdict(list)
        
        terms = dict(nx.get_node_attributes(self.nxgraph, 'name'))
        
        for node in self.nxgraph.nodes():
            
            for node2 in  self.nxgraph.neighbors(node):
                ontology[ str(terms[node]).split(":")[1] ].append( str(terms[node2]).split(":")[1])
                
        for id, example1 in enumerate(ontology.keys()):
            # Write to rdf graph                         
            u = rdflib.term.URIRef('%sTERM%s' % (obo_uri, example1))
            #g.add((u, rdflib.RDF.type, KT.is_a))
            for ex in ontology[example1]:
                annotation_uri = rdflib.term.URIRef('%s%s' % (obo_uri, rdflib.Literal(ex)))
                g.add((u, KT.is_a,annotation_uri ))

        self.rdfgraph = g
        g.serialize(destination=outfile,format='n3')

        
    def return_target_n3(self):

        target_dict = {}
        filenames = [self.cfile+"/"+f for f in os.listdir(self.cfile)]
        for file in filenames:
            with open(file) as f:
                for line in f:
                    target_dict[line.replace("\n","")] = file

        print (target_dict.values())
        
        ## construct target class ontology

                # for id, example1 in enumerate(targetdict.keys()):
            
        #     # Write to rdf graph
            
        #     u = rdflib.term.URIRef('%s%s' % (amp_uri, example1))
        #     g.add((u, rdflib.RDF.type, KT.Example))
        #     g.add((u, KT.class_label, rdflib.Literal(targetdict[example1])))
                        
        #     for ex in ontology[example1]:
        #         annotation_uri = rdflib.term.URIRef('%s%s' % (obo_uri, rdflib.Literal(ex)))
        #         blank = rdflib.BNode()
        #         g.add((u, KT.annotated_with, blank))
        #         g.add((blank, KT.annotation, annotation_uri))
            
        # g.serialize(destination=outfile,format='n3')
        
        return target_dict
    
    def rdf_state(self):
        ## check if rdf graph is valid one
        return 
        

# if __name__ == '__main__':
    
#     converter = rdfconverter("abc","data")
#     converter.return_background_knowledge()
    


    ## get rdf and run Hedwig!

    
 #   request.execute_query_orto(source)
  #  request.draw_graph_ortolog(labs=True)
#    request.execute_query_orto(source)

# import sys
# import rdflib
# from collections import defaultdict
# ## input files here..


# data_file = 'candidates.csv'
# mapping_file = 'gene_association.mgi'
# targets = {}

# with open(data_file) as f:
#     lines = f.readlines()
#     for line in lines:
#         targets[line.split(",")[0]] = line.split(",")[1].replace("\n","")

  
# for k,v in targets.items():
#     print(k,v)
# tempGO = defaultdict(list)
# for line in open(mapping_file,'r').readlines():
#     if not line.startswith("!"):    
#         parts = line.split("\t")[4]
#         for k in targets.keys():
#             if k != 'gene' and k in line:                
#                 tempGO[k].append(line.split("\t")[4])

# #print(tempGO)

# ## from this point on, construct a rdf graph!


# g = rdflib.graph.Graph()
# KT = rdflib.Namespace('http://kt.ijs.si/hedwig#')
# amp_uri = 'http://kt.ijs.si/ontology/hedwig#'
# obo_uri = "http://purl.obolibrary.org/obo/"
# AMP = rdflib.Namespace(amp_uri)


# for id, example1 in enumerate(targets.keys()):
#     # Write to rdf graph
#     u = rdflib.term.URIRef('%sgene%s' % (amp_uri, example1))
#     g.add((u, rdflib.RDF.type, KT.Example))
#     g.add((u, KT.class_label, rdflib.Literal(targets[example1])))
#     for ex in tempGO[example1]:
#         annotation_uri = rdflib.term.URIRef('%s%s' % (obo_uri, rdflib.Literal(ex)))

#         blank = rdflib.BNode()
#         g.add((u, KT.annotated_with, blank))
#         g.add((blank, KT.annotation, annotation_uri))


# g.serialize(destination="backgroundONT4.n3",format='n3')

# ## hedwig run> 

# p#hedwig bk/ examples/chr1_clusters_fix.n3 -o 393_clusters_w_hierarchy_fix.txt -A 0.05 -a fwer -l

    
# import sys
# import rdflib
# from collections import defaultdict
# ## input files here..


# mapping_file = 'kegg2go'


# ### kegg and ontology files..
# tempGO = defaultdict(list)
# for line in open(mapping_file,'r').readlines():
#     if not line.startswith("!"):    
#         parts = line.split(";")
#         #print(parts[1].replace("\n",""))        
#         if parts[1] != "" or parts[1] != None:
#             tempGO[parts[0].split(":")[1].split(">")[0].replace(" ","")].append(parts[1].replace("\n",""))

# #print (tempGO)
# ## from this point on, construct a rdf graph!
# KT = rdflib.Namespace('http://kt.ijs.si/hedwig#')
# g = rdflib.graph.Graph()
# obo_uri = "http://purl.obolibrary.org/obo/"
# AMP = rdflib.Namespace(obo_uri)

# # # simply go through dict and for each key, add items as predicate is_a
# for id, example1 in enumerate(tempGO.keys()):
#     # Write to rdf graph
#     graphkey = example1

#     u = rdflib.term.URIRef('%sTERM%s' % (obo_uri, graphkey))
#     #g.add((u, rdflib.RDF.type, KT.is_a))
#     for ex in tempGO[example1]:
#         annotation_uri = rdflib.term.URIRef('%s%s' % (obo_uri, rdflib.Literal(ex.replace(" ",""))))

#         g.add((u, KT.is_a,annotation_uri ))

# #g.serialize(format='n3')
# g.serialize(destination="KEGGbk.n3",format='n3')
