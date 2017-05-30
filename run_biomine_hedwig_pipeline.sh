
## this is an example run script for a thypical workflow

if [ "$1" == "--execute"  ]
then
    python3 get_bk.py --step_size 10 --output_name $2 ## looks into data folder
    python3 g2o.py --input_graph "graph_datasets/biomine"$2"graph.gpickle" --percentile 50 --ontology_id $2.n3 ## samples and BK folders
    python2 hedwig/hedwig BK/ samples/$2".n3" -l -o OUTPUT/$2 -A 0.5 ## output folder

elif [ "$1" == "--clean" ]
then
    rm -rvf BK/*
    rm -rvf samples/*
    rm -rvf OUTPUT/*
fi
     
