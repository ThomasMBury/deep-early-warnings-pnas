#==============
# Run AUTO on generated model
#==============


# Import packages
import numpy as np
import csv
import random




# Make directory for output data
!mkdir -p output_auto

print('Running AUTO')

# Labels of all parameters in model
par_labels = ['a'+str(i) for i in np.arange(1,11)]+['b'+str(i) for i in np.arange(1,11)]

# Import parameter data as an array
with open('output_model/pars.csv', 'r') as csvfile:
    pars_raw = list(csv.reader(csvfile))
pars_list = [float(p[0]) for p in pars_raw]
pars_array = np.array(pars_list)

# Put into dictionary form for AUTO - note par(11) is reserved
p = dict(zip(np.concatenate((np.arange(1,11), np.arange(12,22))), pars_array))

    

# Import equilibrium data as an array
with open('output_model/equi.csv', 'r') as csvfile:
    equi_raw = list(csv.reader(csvfile))   
      
equi_list = [float(e[0]) for e in equi_raw]
u = np.array(equi_list)
print "Equilibrium is ", u[0], u[1]

# Loop through parameter labels *that are non-zero*
index_zero = np.where(pars_array!=0)[0]
for par in [par_labels[j] for j in index_zero]:
    print('\nBifurcation continuation with parameter '+par)

    
    # Load xxx.f90 and c.xxx files into AUTO
    model = load('model')
    
    # Load equi and pars into AUTO
    model = load(u, PAR=p, ICP=par, UZSTOP={par:[-5,5]})
    
    # Run and store results in Python variable out
    out = run(model)
    
    # Save out to bifurcation files b.out, s.out and d.out
    save(out,'out'+par)
        
    # Remove s.out and d.out (! uses bash in an AUTO file)
    !rm s.out*
    !rm d.out*
        
    # Move b.out to director output_auto
    !mv b.out* output_auto
    
    # Clean the directory
    print "Clean the directory"
    clean()
    
# Make space
print("\nEnd AUTO\n\n")
        
