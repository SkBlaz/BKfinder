
## this is an example run script for a thypical workflow

if [ "$1" == "--execute"  ] ## permutations + learning graph
then
    
    python3 get_bk.py --step_size 10 --output_name $2 --term_list $3   ## looks into data folder
    
    python3 g2o.py --input_graph "graph_datasets/"$2".gpickle" --percentile 50 --ontology_id $2.n3 ## samples and BK folders
    
    python3 make_subgroups.py --input_file data/snps_clean.list --repetitions 200 --target_folder samples/bruteforce.n3 --max_group_size 20
    
    python2 hedwig/hedwig BK/ samples/$2".n3" -l -o OUTPUT/$2 -A 0.5 ## output folder
    cat OUTPUT/$2
    
elif [ "$1" == "--clean" ]
then
    rm -rvf BK/*
    rm -rvf samples/*
    rm -rvf OUTPUT/*
    rm -rvf query/*

elif [ "$1" == "--learn" ] ## this learns from permutations
then
    python3 g2o.py --input_graph "graph_datasets/"$2".gpickle" --percentile 95 --ontology_id $2.n3 --step_size 1 ## samples and BK folders

    python3 make_subgroups.py --input_file data/snps_clean.list --repetitions 2 --target_folder samples/$2.n3 --max_group_size 15
    
    python2 hedwig/hedwig BK/ samples/$2".n3" -o OUTPUT/$2 -l -A 0.5 -C ## output folder
    cat OUTPUT/$2 

    #    rm -rvf samples/*

elif [ "$1" == "--learn_custom" ] ### this learns from different size bins
then

    bash run_biomine_hedwig_pipeline.sh --clean
    python3 filter_snps.py --bins $3  ## kok delov
    python3 g2o.py --input_graph "graph_datasets/"$2".gpickle" --percentile 95 --ontology_id $2.n3 --step_size 1 --make_samples true
    python2 hedwig/hedwig BK/ samples/$2".n3" -o OUTPUT/$2 -l -A 1 -C ## output folder
    cat OUTPUT/$2 
    ## the point here is, this works..
    ## 
    
elif [ "$1" == "--hedwig_only" ]
then
    python2 hedwig/hedwig $2 $3 -o OUTPUT/$4 -l -A 1 -C ## output folder
    cat OUTPUT/$4 


elif [ "$1" == "--clusters" ]
then

    bash run_biomine_hedwig_pipeline.sh --clean

    python3 similarity_clustering.py --input_graph graph_datasets/snpsstep1.gpickle --input_nodelist data/snps_clean.list --number_clusters $2 --output_folder query    
    
    ## do this when query is already there..
    python3 g2o.py --input_graph graph_datasets/snpsstep1.gpickle --percentile 90 --step_size 1 --heuristic degree --ontology_id clustering.n3 --make_samples t

    python2 hedwig/hedwig BK/autogenclustering.n3 samples/clustering.n3 -o OUTPUT/clustering -l -A 1 --adjust=none --support=0 --beam=10
    cat OUTPUT/clustering


elif [ "$1" == "--community" ]
then

    cd data
    #wget http://purl.obolibrary.org/obo/go/go-basic.obo
    cd ..

    echo "Generating background knowledge"
    python3 obo2n3.py --input_obo data/go-basic.obo  --output_n3 BK/uniprot.n3
    
    echo "Subgroup identification"    
    python3 community_clustering.py --input_graph graph_datasets/snpsstep1.gpickle --input_nodelist data/snps_clean.list --ontology_id samples/community_samples.n3 --nc 2 --input_mapping data/goa_human.gaf
    
    echo "Hedwig run.."
    python2 hedwig/hedwig BK/ samples/test2.n3 -o OUTPUT/community_rules -l --adjust=none --support=0.1 --beam=50

    cat OUTPUT/community_rules
     
fi
     
# python3 obo2n3.py --input_obo ~/Documents/go.obo --output_n3 BK/uniprot.n3
# sudo python2 hedwig/hedwig BK/uniprot.n3 samples/mappedONTO.n3 -o OUTPUT/kclique -l --adjust=none --support=0 --beam=50


