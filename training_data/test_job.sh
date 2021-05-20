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
#SBATCH --time=0-00:10:00
#SBATCH --output=Jobs/output/job-%j.out
#SBATCH --ntasks=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=tbury@uwaterloo.ca


echo Running test script on Hagrid

# Create a test output file
touch output_test3.txt

# Move it to Hagrid storage node
mv output_test3.txt /scratch/tbury


