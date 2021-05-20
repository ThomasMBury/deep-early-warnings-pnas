#!/bin/bash

# # Thomas Bury
# # PhD Candidate
# # Bauch computational epidemiology research group
# # Department of Applied Mathematics
# # Faculty of Mathematics
# # University of Waterloo


# Batch number
batch_num=1


# Make job-specific directory and move to this directory
mkdir -p output/batch$batch_num
cd output/batch$batch_num

# Set up timer
start=`date +%s`

echo Job released


# Define variables that count numbers of bifurcations
bif_max=2 # Number of each type of bifurcation to generate
batch_num=1 # ID of batch
hopf_count=0
fold_count=0
branch_count=0
null_count=0
null_h_count=0
null_f_count=0
null_b_count=0


# While loop
while [ $hopf_count -lt $bif_max ] || [ $fold_count -lt $bif_max ] || [ $branch_count -lt $bif_max ] || [ $null_count -lt $bif_max ]
do
printf "\nBifurcation counts\n"
printf "hopf_count = $hopf_count, fold_count = $fold_count, branch_count = $branch_count, null_count = $null_count"
printf "\n\n"


# Generate a model and output equi.csv, pars.csv
echo Run gen_model.py
python3 ../../gen_model.py


# Run bifurcation continuation using AUTO, output b.out files for each varied parameter
# (Make sure runs using Python 2)
# Copy auto model and constants files to job-specific directory
cp ../../c.model c.model
cp ../../model.f90 model.f90
echo Run run_cont.auto
auto ../../run_cont.auto

# Remove unnecessary files
rm -f c.model
rm -f model.f90

# For each parameter with a bifurcation, run simulations up to the
# bifurcation point, and output 500 points prior to the transition.
# Also run a null case where parameters are fixed.
echo Run stoch_sims.py
python3 ../../stoch_sims.py $hopf_count $fold_count $branch_count $null_h_count $null_f_count $null_b_count $bif_max $batch_num


# Update counting variables
hopf_count=$(sed '1q;d' output_counts/list_counts.txt)
fold_count=$(sed '2q;d' output_counts/list_counts.txt)
branch_count=$(sed '3q;d' output_counts/list_counts.txt)
null_h_count=$(sed '4q;d' output_counts/list_counts.txt)
null_f_count=$(sed '5q;d' output_counts/list_counts.txt)
null_b_count=$(sed '6q;d' output_counts/list_counts.txt)
null_count=$((null_h_count+null_f_count+null_b_count))


# Remove old model, auto and simulation files to save space
rm -r output_model
rm -r output_auto

done

# Convert label data and split into training, test, validation
echo "Convert data to correct form for training"
python3 ../../to_traindata.py $bif_max $batch_num

# Remove single label files
rm output_labels/label*


# Compute residual dynamics and standard EWS from each simulation
echo "Compute EWS"
python3 ../../compute_ews.py $bif_max $batch_num


# End timer
end=`date +%s`
runtime=$((end-start))
echo "Job successfully finished in time of $runtime" seconds.

# Change back to original directory
cd ../../


