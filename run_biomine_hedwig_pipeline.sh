
## this is an example run script for a thypical workflow

python3 get_bk.py --step_size 10 --output_name $1 ## looks into data folder
python3 g2o.py --input_graph graph_datasets/biomine$1graph.gpickle --percentile 50 --data_input_id $1 ## samples and BK folders
python2 hedwig/hedwig BK/ samples/$1.n3 -l -o OUTPUT/$1 -A 0.8 ## output folder
