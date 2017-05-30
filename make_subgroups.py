### this small script takes a term list as input and generates different combinations of inpute terms - candidate subgroups

import numpy as np
import argparse
import rdflib

def return_subgroup(infile,repetitions,outfolder,max_size):

        
    with open(infile, 'r') as myfile:
        data=myfile.read().split('\n')

    if max_size != None:
        pass
    else:
        max_size = len(data)
        
    g = rdflib.graph.Graph()
    KT = rdflib.Namespace('http://kt.ijs.si/hedwig#')
    amp_uri = 'http://kt.ijs.si/ontology/hedwig#'
    obo_uri = "http://purl.obolibrary.org/obo/"
    AMP = rdflib.Namespace(amp_uri)

    print("Monte carlo sampling in place..")
    for repetition in range(repetitions):
        indices = np.random.choice(len(data), np.random.randint(max_size, size=1), replace=False)
        subset = [data[i] for i in indices]
              
        ## Write to rdf graph
        u = rdflib.term.URIRef('%sexample%s' % (amp_uri, repetition))
        g.add((u, rdflib.RDF.type, KT.Example))
        g.add((u, KT.class_label, rdflib.Literal("candidate_"+str(repetition))))
        
        for ex in subset:                  
            annotation_uri = rdflib.term.URIRef('%s%s' % (obo_uri, rdflib.Literal(ex)))
            blank = rdflib.BNode()
            g.add((u, KT.annotated_with, blank))
            g.add((blank, KT.annotation, annotation_uri))
            
    g.serialize(destination=outfolder,format='n3')
    
    print("Samples constructed..")
if __name__ == '__main__':

    parser_init = argparse.ArgumentParser()
    parser_init.add_argument("--input_file", help="Term file.")
    parser_init.add_argument("--repetitions", help="Monte carlo repetitions.")
    parser_init.add_argument("--target_folder", help="Target dir.")
    parser_init.add_argument("--max_group_size", help="group size maximum.")
    
    parser = parser_init.parse_args()
    if parser.max_group_size:
        return_subgroup(parser.input_file,int(parser.repetitions),parser.target_folder,max_size=int(parser.max_group_size))
    else:
        return_subgroup(parser.input_file,int(parser.repetitions),parser.target_folder,max_size=None)
    

    

    
