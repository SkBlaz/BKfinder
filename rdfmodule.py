## this is the RDF to NetworkX converter class..

import rdflib
import sys
from collections import defaultdict

class rdfconverter:
    def __init__(self, nxgraph, candidates_1,candidates_2=None):
        
        self.nxgraph = nxgraph        
        self.candidates_1 = candidates_1
        self.candidates_2 = candidates_2
        
    def return_background_knowledge(self):

#        return_target_n3   # this is to generate targets
        ## for starters some default parameters..
        g = rdflib.graph.Graph()
        KT = rdflib.Namespace('http://kt.ijs.si/hedwig#'
        amp_uri = 'http://kt.ijs.si/ontology/hedwig#'
        obo_uri = "http://purl.obolibrary.org/obo/"
        AMP = rdflib.Namespace(amp_uri)

        for id, example1 in enumerate(targets.keys()):
            # Write to rdf graph
            u = rdflib.term.URIRef('%sgene%s' % (amp_uri, example1))
            g.add((u, rdflib.RDF.type, KT.Example))
            g.add((u, KT.class_label, rdflib.Literal(targets[example1])))
            for ex in tempGO[example1]:
                annotation_uri = rdflib.term.URIRef('%s%s' % (obo_uri, rdflib.Literal(ex)))
                blank = rdflib.BNode()
                g.add((u, KT.annotated_with, blank))
                g.add((blank, KT.annotation, annotation_uri))

        ## run hedwig directly!
        g.serialize(destination="backgroundONT4.n3",format='n3')
        
    def return_target_n3(self):
        #this function will be able to get target examples, sufficiently recoded.
                              ## this reads a file, where each column is a separate class.
        #self.targets

    def rdf_state(self):
        ## check if rdf graph is valid one
    
        


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

    
