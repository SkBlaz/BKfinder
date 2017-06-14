### this algorithm is capable of community clustering


#import community
import networkx as nx
import argparse
import rdflib
from collections import defaultdict
import itertools
import community

def community_cluster(G, termlist):

    ## this is the louvain method..
    Gx = nx.Graph()
    nodes = G.nodes(data=False)
    edges = G.edges(data=False)
    Gx.add_nodes_from(nodes)
    Gx.add_edges_from(edges)
    communities = community.best_partition(Gx)
    
    # communities = nx.k_clique_communities(G, ncom)
    # communities = itertools.islice(communities,4)
    
    return communities

if __name__ == '__main__':

    parser_init = argparse.ArgumentParser()
    parser_init.add_argument("--input_graph", help="Graph in gpickle format.")
    parser_init.add_argument("--input_nodelist", help="Nodelist input..")
    parser_init.add_argument("--ontology_id", help="prediction_file..")
    parser_init.add_argument("--input_mapping", help="prediction_file..")
    
    parsed = parser_init.parse_args()

    uniGO = defaultdict(list)    
    with open(parsed.input_mapping) as im:
        for line in im:
            parts = line.split("\t")
            try:
                uniGO[parts[1]].append(parts[4])
            except:
                pass
    
    G = nx.read_gpickle(parsed.input_graph)
    termlist = []

    with open(parsed.input_nodelist) as nl:
        for line in nl:
            parts = line.strip().split()
            termlist.append(parts[0])

    predictions = community_cluster(G,termlist)

    g = rdflib.graph.Graph()
    KT = rdflib.Namespace('http://kt.ijs.si/hedwig#')
    amp_uri = 'http://kt.ijs.si/ontology/hedwig#'
    obo_uri = "http://purl.obolibrary.org/obo/"
    AMP = rdflib.Namespace(amp_uri)

    ## FOR PAIR, add to class community, node.split(), mapped term to class..

    ntuple = [(k,v) for k,v in predictions.items()]
    id_identifier = 0
    
    for node, com in ntuple:
        node = node.split(":")[1]
        id_identifier += 1        
        u = rdflib.term.URIRef('%sexample%s' % (amp_uri, com))
        g.add((u, rdflib.RDF.type, KT.Example))
        g.add((u, KT.class_label, rdflib.Literal(str(com)+"_community")))
        for goterm in uniGO[node]:  
            annotation_uri = rdflib.term.URIRef('%s%s' % (obo_uri, rdflib.Literal(goterm)))
            blank = rdflib.BNode()
            g.add((u, KT.annotated_with, blank))
            g.add((blank, KT.annotation, annotation_uri))

    g.serialize(destination=parsed.ontology_id,format='n3')    
    
    # print ("Sample generation..")
    # for com, community in enumerate(predictions):
    #     nodes = [el.split(":")[1] for el in list(community)]
    #     u = rdflib.term.URIRef('%sexample%s' % (amp_uri, com))
    #     for ex, node in enumerate(nodes):
    #         g.add((u, rdflib.RDF.type, KT.Example))
    #         g.add((u, KT.class_label, rdflib.Literal(str(com)+"_community")))  
    #         for goterm in uniGO[node]:                  
    #             annotation_uri = rdflib.term.URIRef('%s%s' % (obo_uri, rdflib.Literal(goterm)))
    #             blank = rdflib.BNode()
    #             g.add((u, KT.annotated_with, blank))
    #             g.add((blank, KT.annotation, annotation_uri))
            
    # g.serialize(destination=parsed.ontology_id,format='n3')
        

    # f = open(str(parsed.output_folder)+"/"+str(com)+"cluster", 'w')
    # outdata = "\n".join(nodes)
    # f.write(outdata)
    # f.close()
    # rdfpart = rm.rdfconverter(None,"query")
    # rdfpart.return_target_n3("samples/"+parsed.ontology_id)
