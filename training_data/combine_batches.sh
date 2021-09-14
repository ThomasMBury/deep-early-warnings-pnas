#!/bin/bash

# Script to stack label and group data from each batch
# and copy all simulation and residual data to the same folder



# Command line arguments
num_batches=$1 # number of batches generated
ts_len=$2 # time series length


# Run Python file to stack the label and group data
python3 stack_labels_groups.py $num_batches $ts_len

# Move time series data from batches to combined directory
mkdir -p output/ts_$ts_len/combined/output_sims
mkdir -p output/ts_$ts_len/combined/output_resids

let min=1
let max=num_batches

for i in $(seq $min $max)
do
   cp output/ts_$ts_len/batch$i/output_sims/* output/ts_$ts_len/combined/output_sims
   cp output/ts_$ts_len/batch$i/output_resids/* output/ts_$ts_len/combined/output_resids
done

# Zip the folders
cd output/ts_$ts_len/combined
zip -r output_sims.zip output_sims
zip -r output_resids.zip output_resids

## Delete the originals
# rm -r output_sims output_resids

cd ../../../