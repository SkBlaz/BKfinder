## this will be the python interface for command line execution..

###### example
#python3 CBSD.py --step_size 10 --knowledge_graph graph_datasets/epigenetics.gpickle --term_list data/epigenetics.list --ontology_BK data/go-basic.obo --output_BK BK/uniprot.n3 --n3_samples samples/epiSamples.n3 --gaf_mapping data/goa_human.gaf --rule_output OUTPUT/epi.txt
######

from get_bk import *
from obo2n3 import *
from community_clustering import *
import subprocess
import argparse

if __name__ == '__main__':

    parser_init = argparse.ArgumentParser()
    parser_init.add_argument("--step_size", help="When building the graph..")
    parser_init.add_argument("--knowledge_graph", help="Nodelist input..")
    parser_init.add_argument("--term_list", help="prediction_file..")
    parser_init.add_argument("--ontology_BK", help="prediction_file..")
    parser_init.add_argument("--output_BK", help="prediction_file..")
    parser_init.add_argument("--n3_samples", help="prediction_file..")
    parser_init.add_argument("--gaf_mapping", help="prediction_file..")
    parser_init.add_argument("--rule_output", help="prediction_file..")
    
    parsed = parser_init.parse_args()
    source = read_example_datalist(parsed.term_list,whole=True)

    hedwig_command = "python2 hedwig/hedwig BK/ "+parsed.n3_samples+" -o "+parsed.rule_output+" -l --adjust=none --beam=50"

    
    if parsed.step_size:

        ## generate and learn
        
        request = make_request()
        result_graph = request.execute_query_inc(source,div=int(parsed.step_size),connected=False)

        print ("STEP 1: Writing pickle datadump..")        
        nx.write_gpickle(result_graph, parsed.knowledge_graph)

        print("STEP 2: Background knowledge generation")        
        obo2n3(parsed.ontology_BK, parsed.output_BK)

        print ("STEP 3: subgroup identification")
        community_cluster_n3(parsed.knowledge_graph,parsed.term_list,parsed.gaf_mapping,parsed.n3_samples)
        
        print ("STEP 4: Learning")
        print("HEDWIG: "+hedwig_command)
        process = subprocess.Popen(hedwig_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output)
                                     
    else:

        ## only learn
        print("STEP 2: Background knowledge generation")        
        obo2n3(parsed.ontology_BK, parsed.output_BK)

        print ("STEP 3: subgroup identification")
        community_cluster_n3(parsed.knowledge_graph,parsed.term_list,parsed.gaf_mapping,parsed.n3_samples)
        
        print ("STEP 4: Learning")
        print("HEDWIG: "+hedwig_command)
        process = subprocess.Popen(hedwig_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        print(output)
        
    
