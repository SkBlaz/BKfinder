### this script converts a uniprot mapping file to the gene ontology term file..

import community
import networkx as nx
import argparse
import rdfmodule as rm
import rdflib
from collections import defaultdict

if __name__ == '__main__':


    parser_init = argparse.ArgumentParser()
    parser_init.add_argument("--input_mapping", help="Graph in gpickle format.")
    parser_init.add_argument("--output_n3", help="Nodelist input..")
    parsed = parser_init.parse_args()

    uniGO = defaultdict(list)    
    with open(parsed.input_mapping) as im:
        for line in im:
            parts = line.split("\t")
            try:
                uniGO[parts[1]].append(parts[4])
            except:
                pass
    
    print(len(uniGO.keys()))

    g = rdflib.graph.Graph()
    KT = rdflib.Namespace('http://kt.ijs.si/hedwig#')
    amp_uri = 'http://kt.ijs.si/ontology/hedwig#'
    obo_uri = "http://purl.obolibrary.org/obo/"
    AMP = rdflib.Namespace(amp_uri)        

    for k,v in uniGO.items():                    
        u = rdflib.term.URIRef('%s%s' % (obo_uri, k))
        for val in v:
            annotation_uri = rdflib.term.URIRef('%s%s' % (obo_uri, rdflib.Literal(val)))
            g.add((u, rdflib.RDFS.subClassOf,annotation_uri))
            
    g.serialize(destination=parsed.output_n3,format="n3")
