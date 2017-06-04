## this script reads the ePPISNP dataset and emits groups of identifiers by size groups
## get all values, sort and split with numpy

import numpy as np
from collections import defaultdict
from subprocess import call
import argparse

call(["rm", "-rvf","query/*"])

parser_init = argparse.ArgumentParser()
parser_init.add_argument("--bins", help="Bin split..")
parsed = parser_init.parse_args()
    
termnames = "graph_datasets/datafile.tsv"
term_list = defaultdict(list)

with open(termnames) as tf:
    for line in tf:
        line_parts = line.split()
        protein1 = line_parts[0]
        protein2 = line_parts[3]
        size = line_parts[4]
        if ":" not in protein1:
            term_list[protein1].append(size)
        if ":" not in protein2:
            term_list[protein2].append(size)

all_lengths=[]
for k,v in term_list.items():
    term_list[k] = set(term_list[k])
    for term in term_list[k]:
        all_lengths.append(int(term))

sorted_array = np.sort(all_lengths, axis=None)
three_parts = np.array_split(sorted_array, int(parsed.bins))

for idx,part in enumerate(three_parts):
    current_outname = "part:"+str(idx)
    current_termlist = []
    for k,val in term_list.items():        
        for el in val:
            if int(el) in list(part):                
               current_termlist.append(k)
    f = open("query/"+current_outname, 'w')
    f.write("\n".join(set(current_termlist)))
    f.close() 


