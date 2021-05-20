#!/bin/bash

# # Thomas Bury
# # PhD Candidate
# # Bauch computational epidemiology research group
# # Department of Applied Mathematics
# # Faculty of Mathematics
# # University of Waterloo

#SBATCH --account=hagrid
#SBATCH --partition=hagrid_long
#SBATCH --mem=1000MB
#SBATCH --time=0-01:00:00
#SBATCH --output=output/stdout/zip-%j.out
#SBATCH --ntasks=1
#SBATCH --mail-type=END
#SBATCH --mail-user=tbury@uwaterloo.ca


# Label for set of batches (external variable)
batch_set=$1

# Number of batches within each set
num_batches=$2

# Run Python file to concatenate label and group data
python3 combine_batches.py $batch_set $num_batches


# Move time series data from batches to combined directory
mkdir -p output/combined_$batch_set/output_sims
mkdir -p output/combined_$batch_set/output_resids

let min=(batch_set-1)\*num_batches+1
let max=batch_set\*num_batches

for i in $(seq $min $max)
do
   mv output/batch$i/output_sims/* output/combined_$batch_set/output_sims
   mv output/batch$i/output_resids/* output/combined_$batch_set/output_resids
done

# Zip the folders
cd output/combined_$batch_set
zip -r output_sims.zip output_sims
zip -r output_resids.zip output_resids

# Delete the originals
rm -r output_sims output_resids

cd ../../

