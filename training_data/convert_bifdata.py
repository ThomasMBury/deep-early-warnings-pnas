#
# Python function to convert b.out files from AUTO into bifurcation type and point


import pandas as pd


def convert_bifdata(filepath):
    '''
    Function to extract useful information from b.out
    
    Input:
        filepath to b.out
        
    Output
        dict containing
            - bif_param
            - bif_type
            - bif_value
            - branch_values
            
    '''
    
      
    # Read in lines from b.out file
    f = open(filepath, 'r')
    raw_lines = f.readlines()
    f.close()
    
    # Find out bifurcation parameter used
    index_list=[i.find('Active continuation parameter') for i in raw_lines]
    pos = [(i,index_list[i]) for i in range(len(index_list)) if index_list[i]>0]
    # Line with bifurcadtion parameter
    l_temp = raw_lines[pos[0][0]]
    # Select segment with bifurcation parameter
    bif_param = l_temp[pos[0][1]+34:l_temp.find('\n')-1]
    
    
    # Select first branch
    raw1 = []
    for i in range(len(raw_lines)):
        if raw_lines[i][3]=='1':
            raw1.append(raw_lines[i])
    
    # Function to make sure there is an E before the - or +
    def placeE(number):
        index = number.find('E')
        if index!=-1:
            return number
        else:
            index2 = max([number[1:].find(i) for i in ['+','-']])
            # Place an E
            number_out = number[:index2+1]+'E'+number[index2+1:]
            return number_out

    
    # Get point types - convert to integers
    types = [int(raw1[i][12:14]) for i in range(len(raw1))]
    
    # Get bif param values
    bifParam = [float(placeE(raw1[i][21:38])) for i in range(len(raw1))]
    
    # Get x values           
    xVals = [float(placeE(raw1[i][59:76])) for i in range(len(raw1))]
    
    
    # Create DataFrame
    df_branch = pd.DataFrame({'TY':types, 'bp':bifParam, 'x':xVals})
    
    
    # Labels for special points
    # 1,6 - branch point (transcritical)
    # 2,5 - fold bifurcation
    # 3 - Hopf bifurcation
    
    specials=[1,2,3,5,6]

    labels = {1:'BP', 2:'LP', 3:'HB', 5:'LP', 6:'BP'}
    
    # Find bifurcation points along branch
    df_bifs = df_branch[df_branch['TY'].isin(specials)]
    
    # If non-empty
    if df_bifs.size != 0:
        
        # Bifurcation type
        bif_type = labels[df_bifs['TY'].iloc[0]]
        
        # Bifurcation value
        bif_val = df_bifs['bp'].iloc[0]
        
        # Export dictionary
        dic_out = {'type':bif_type, 'value':bif_val, 'bif_param':bif_param, 'branch_vals':xVals}
    
    else: dic_out = {'type':'NA', 'value':0, 'bif_param':bif_param, 'branch_vals':xVals}
    
    return dic_out










