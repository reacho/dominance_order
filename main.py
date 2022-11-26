import copy
import numpy as np

## Some functions

def return_one_base_and_exp_pair(my_line):
    start = 0
    v_base = []
    v_exp  = []
    v_base_intermed = []
    v_exp_intermed  = []
    for cont, my_char in enumerate(my_line):
        #
        if my_char=='^':
            v_base_intermed.append(int(my_line[start:cont]))
            start = cont+1
        if (my_char==',' and my_line[max(cont-1,0):min(cont+1,len(my_line)-1)+1] != '),(') or my_char==')':
            v_exp_intermed.append(int(my_line[start:cont]))
            start = cont+1
        if my_char==',' and my_line[max(cont-1,0):min(cont+1,len(my_line)-1)+1] == '),(':
            v_base.append(v_base_intermed)
            v_exp.append(v_exp_intermed)
            v_base_intermed = []
            v_exp_intermed  = []
            start=cont+2

    v_exp_intermed.append(int(my_line[start:cont+1]))

    v_base.append(v_base_intermed)
    v_exp.append(v_exp_intermed)
    return v_base, v_exp


################################################

def compute_all_sum(v_base, v_exp):
    partial_sum = 0
    v_sum = []
    for base, exp in zip(v_base, v_exp):
        v_sum_aus = []
        for cont_1 in range(len(base)):
            b = base[cont_1]
            e = exp[cont_1]
            for _ in range(e):
                partial_sum += b
                v_sum_aus.append(partial_sum)
        v_sum.append(v_sum_aus)
        
    return v_sum

################################################

def who_is_larger__pair(pair_1, pair_2):
    v_base_1, v_exp_1 = pair_1
    v_base_2, v_exp_2 = pair_2
    my_sum_1 = compute_all_sum(v_base_1, v_exp_1)
    my_sum_2 = compute_all_sum(v_base_2, v_exp_2)
    BOOLEAN_1_LARGER = True
    BOOLEAN_2_LARGER = True
    for list_1, list_2 in zip(my_sum_1, my_sum_2):
        L1 = len(list_1)-1
        L2 = len(list_2)-1

        for cont in range(max(L1,L2)+1):
            if list_1[min(L1,cont)] > list_2[min(L2,cont)]:
                BOOLEAN_2_LARGER = False
            elif list_1[min(L1,cont)] < list_2[min(L2,cont)]:
                BOOLEAN_1_LARGER = False
            if not (BOOLEAN_1_LARGER or BOOLEAN_2_LARGER):
                break
        if not (BOOLEAN_1_LARGER or BOOLEAN_2_LARGER):
            break
    return BOOLEAN_1_LARGER, BOOLEAN_2_LARGER

################################################
################################################

"""
Open
   data_values.txt
and load all the values.

"""

v_all_bases = []
v_all_exps  = []

filepath = 'data_values.txt'
v_line = []
with open(filepath) as fp:
   #line = fp.readline()
   for line in fp.readlines():
      my_line = copy.copy(line.strip())
      # remove first and last parentheses
      my_line = my_line[2:-2]

      this_base, this_exp = return_one_base_and_exp_pair(my_line)
      v_all_bases.append(this_base)
      v_all_exps.append(this_exp)

################################################

"""
Compute the matrix (dominance order)
"""
L = len(list(zip(v_all_bases, v_all_exps)))
results = np.zeros((L,L), dtype=int)

for row in range(L):
    col = row+1
    pair1 = list(zip(v_all_bases, v_all_exps))[row]
    while col<L:
        pair2=list(zip(v_all_bases, v_all_exps))[col]
        BOOLEAN_1_LARGER, BOOLEAN_2_LARGER = who_is_larger__pair(pair1, pair2)
        if BOOLEAN_1_LARGER:
            results[row,col] = 1
        elif BOOLEAN_2_LARGER:
            results[row,col] = -1
        col+=1    

################################################

"""
Compute, plot, and save the dominance order matrix
"""
dominance_order = results - results.transpose()
print(dominance_order)

with open('dominance_order.npy', 'wb') as f:
    np.save(f, dominance_order)