#!/usr/local/bin/python


# Script to release batch jobs sequentially based on successful completion
# to the SLURM scheduler.

# Jobs generate training data for the 500-classifier, with a total of
# 125 batches = 125*4,000 = 500,000 time series

# Output files are zipped prior to sequential job running to save on disk quota


import os
import subprocess
import commands

if not os.path.exists('output'):
    os.makedirs('output/stdout')


# Define number of batches for each submission
num_batches = 25
ts_length = 500

# Submit the first set of jobs
list_jobnums=[]
for i in range(3*num_batches+1,4*num_batches+1):
    cmd = "sbatch run_single_batch.sh {} {}".format(i,ts_length)
    status, jobcmd = commands.getstatusoutput(cmd)
    jobnum=[int(s) for s in jobcmd.split() if s.isdigit()][0]
    # Add to list of job numbers
    list_jobnums.append(jobnum)
    if (status == 0):
        print cmd + "   Job number: {}".format(jobnum)
    else:
        print "Error submitting Job {}".format(jobnum)

# Submit job to combine batch data, zip files
# and delete originals (to keep within disk quota)
list_jobnums_str = [":"+str(i) for i in list_jobnums]
comb_str = "".join(list_jobnums_str)
cmd = "sbatch --depend=afterok"+comb_str+" combine_batches.sh {} {}".format(1,num_batches)
status, jobcmd = commands.getstatusoutput(cmd)
zip_jobnum=[int(s) for s in jobcmd.split() if s.isdigit()][0]
print cmd + "    Job number: {}".format(zip_jobnum)



# Submit the second set of (dependent) jobs
list_jobnums2=[]
for i in range(4*num_batches+1,5*num_batches+1):
    cmd = "sbatch --depend=afterok:{} run_single_batch.sh {} {}".format(zip_jobnum,i,ts_length)
    status, jobcmd = commands.getstatusoutput(cmd)
    jobnum=[int(s) for s in jobcmd.split() if s.isdigit()][0]
	# Add to list of job numbers
    list_jobnums2.append(jobnum)
    if (status == 0 ):
        print cmd + "    Job number: {}".format(jobnum)
    else:
        print "Error submitting Job"
            
# Submit job to combine batch data, zip files
# and delete originals (to keep within disk quota)
list_jobnums_str = [":"+str(i) for i in list_jobnums2]
comb_str = "".join(list_jobnums_str)
cmd = "sbatch --depend=afterok"+comb_str+" combine_batches.sh {} {}".format(2,num_batches)
status, jobcmd = commands.getstatusoutput(cmd)
zip_jobnum=[int(s) for s in jobcmd.split() if s.isdigit()][0]
print cmd + "    Job number: {}".format(zip_jobnum)






# Submit the third set of (dependent) jobs
list_jobnums3=[]
for i in range(2*num_batches+1,3*num_batches+1):
   cmd = "sbatch --depend=afterok:{} run_single_batch.sh {} {}".format(zip_jobnum,i,ts_length)
   status, jobcmd = commands.getstatusoutput(cmd)
   jobnum=[int(s) for s in jobcmd.split() if s.isdigit()][0]
   # Add to list of job numbers
   list_jobnums3.append(jobnum)
   if (status == 0 ):
       print cmd + "    Job number: {}".format(jobnum)
   else:
       print "Error submitting Job"
         
# Submit job to combine batch data, zip files
# and delete originals (to keep within disk quota)
list_jobnums_str = [":"+str(i) for i in list_jobnums3]
comb_str = "".join(list_jobnums_str)
cmd = "sbatch --depend=afterok"+comb_str+" combine_batches.sh {} {}".format(3,num_batches)
status, jobcmd = commands.getstatusoutput(cmd)
zip_jobnum=[int(s) for s in jobcmd.split() if s.isdigit()][0]
print cmd + "    Job number: {}".format(zip_jobnum)
     
     
        


# Submit the fourth set of (dependent) jobs
list_jobnums4=[]
for i in range(3*num_batches+1,4*num_batches+1):
    cmd = "sbatch --depend=afterok:{} run_single_batch.sh {} {}".format(zip_jobnum,i,ts_length)
    status, jobcmd = commands.getstatusoutput(cmd)
    jobnum=[int(s) for s in jobcmd.split() if s.isdigit()][0]
    Add to list of job numbers
    list_jobnums4.append(jobnum)
    if (status == 0 ):
        print cmd + "    Job number: {}".format(jobnum)
    else:
        print "Error submitting Job"
    
# Submit job to combine batch data, zip files
# and delete originals (to keep within disk quota)
list_jobnums_str = [":"+str(i) for i in list_jobnums4]
comb_str = "".join(list_jobnums_str)
cmd = "sbatch --depend=afterok"+comb_str+" combine_batches.sh {} {}".format(4,num_batches)
status, jobcmd = commands.getstatusoutput(cmd)
zip_jobnum=[int(s) for s in jobcmd.split() if s.isdigit()][0]
print cmd + "    Job number: {}".format(zip_jobnum)




# Submit the fifth set of (dependent) jobs
list_jobnums5=[]
for i in range(4*num_batches+1,5*num_batches+1):
    cmd = "sbatch --depend=afterok:{} run_single_batch.sh {}".format(zip_jobnum,i,ts_length)
    status, jobcmd = commands.getstatusoutput(cmd)
    jobnum=[int(s) for s in jobcmd.split() if s.isdigit()][0]
    Add to list of job numbers
    list_jobnums5.append(jobnum)
    if (status == 0 ):
        print cmd + "    Job number: {}".format(jobnum)
    else:
        print "Error submitting Job"
    

# Submit job to combine batch data, zip files
# and delete originals (to keep within disk quota)
list_jobnums_str = [":"+str(i) for i in list_jobnums5]
comb_str = "".join(list_jobnums_str)
cmd = "sbatch --depend=afterok"+comb_str+" combine_batches.sh {} {}".format(5,num_batches)
status, jobcmd = commands.getstatusoutput(cmd)
zip_jobnum=[int(s) for s in jobcmd.split() if s.isdigit()][0]
print cmd + "    Job number: {}".format(zip_jobnum)







