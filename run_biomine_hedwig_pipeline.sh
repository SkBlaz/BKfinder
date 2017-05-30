
## this is an example run script for a thypical workflow

if [ "$1" == "--execute"  ]
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

elif [ "$1" == "--learn" ]
then
    python3 g2o.py --input_graph "graph_datasets/"$2".gpickle" --percentile 95 --ontology_id $2.n3 ## samples and BK folders

    python3 make_subgroups.py --input_file data/snps_clean.list --repetitions 15 --target_folder samples/$2.n3 --max_group_size 15
    
    python2 hedwig/hedwig BK/ samples/$2".n3" -o OUTPUT/$2 -l -A 0.5 -C ## output folder
    cat OUTPUT/$2 

#    rm -rvf samples/*
fi
     
