import os
import sys
import csv

[input_file, top_10_occupation_path, top_10_states_path] = sys.argv[1:]

#print(input_file)
#print(top_10_occupation_path)
#print(top_t10_states_path)


# 

#os.getcwd()
#os.chdir('../')
#os.chdir('/Users/jacklok/Desktop/Career/Insight/h1b_statistics-master/insight_testsuite/tests/test_1/input')
#with open('h1b_input.csv') as csv_file:

with open(input_file) as csv_file:
    reader = csv.reader(csv_file, delimiter=";", strict=False)
    result = []
    for row in reader:
        if row == []:
            break
        result += [row]

def init_list_of_objects(size):
    list_of_objects = list()
    for i in range(0,size):
        list_of_objects.append( list() ) #different object reference each time
    return list_of_objects

        
keys = result[0]
keys = [k.upper() for k in keys]
a = init_list_of_objects(len(keys))     
for i in range(len(keys)):
    for j in range(1, len(result)):
        a[i].append(result[j][i])   
        
dicts = {}
values = a
for i in range(len(keys)):
    dicts[keys[i]] = values[i]
    
### Top 10 Occupations ###

# Extract needed keys and values from raw data
socname = [s for s in keys if "SOC" in s and "NAME" in s]  # find SOC Name
socname = next(iter(socname))

cstatus = [c for c in keys if "STATUS" in c] # find Case Status
cstatus = next(iter(cstatus))

socname_ls = [k.upper() for k in dicts[socname]]
cstatus_ls = [k.upper() for k in dicts[cstatus]]

occ_pair = {}
for k, v in zip(socname_ls, cstatus_ls):
   occ_pair.setdefault(k, []).append(v)    

# Compute count
from collections import Counter
cert_count = [] 
for i in range(len(occ_pair.keys())):
    sequence_of_status = list(occ_pair.values())[i]
    counts = Counter()
    for certified in sequence_of_status:
       counts.update(word.strip('.,?!"\'- ').lower() for word in certified.split())       
    cert_count.append(counts['certified'])
cert_count

# Compute percentage
totalcert = sum(cert_count)
percent_cert = [x * 100 / totalcert for x in cert_count]

from decimal import *
percent_cert = [float(Decimal("%.1f" % e)) for e in percent_cert]
percent_cert = list(map("{}%".format, percent_cert))

occ_list = occ_pair.keys()

cert_count, occ_list, percent_cert = zip(*sorted(zip(cert_count, occ_list, percent_cert), reverse=True))
cert_count = list(cert_count)
occ_list = list(occ_list)
percent_cert = list(percent_cert)

# Compile the top 10 occupations, their counts, and percent by order.
final = init_list_of_objects(3)
if len(occ_list) >=10:
   final[0] = occ_list[0:10]
   final[1] = cert_count[0:10]
   final[2] = percent_cert[0:10]
else:
   length = len(occ_list)
   final[0] = occ_list[0:length]
   final[1] = cert_count[0:length]
   final[2] = percent_cert[0:length]
   if len(set(final[1]))< len(final[1]):
       l = final[1]
       l = list(set([x for x in l if l.count(x) > 1]))
       for i in l:
           position = [index for index, value in enumerate(final[1]) if value == i]
           final[0][position[0]:position[-1]+1] = sorted(final[0][position[0]:position[-1]+1])
           final[2][position[0]:position[-1]+1] = sorted(final[2][position[0]:position[-1]+1])
final[1] = [str(itm) for itm in final[1]]
       

final = list(zip(final[0], final[1], final[2]))
final.insert(0, ['TOP_OCCUPATIONS', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE'])
final = [list(i) for i in final]


for i in range(len(final)):
    final[i] = ';'.join(final[i])

# Write a new text file into output folder
with open(top_10_occupation_path, 'w') as f:
    for item in final:
        f.write("%s\n" % item)


### Top 10 States ###
        
# Extract needed keys and values from raw data
workstate = [s for s in keys if "WORK" in s and "STATE" in s]  # find Work State
workstate  = next(iter(workstate))
workstate_ls = [k.upper() for k in dicts[workstate]]

state_pair = {}
for k, v in zip(workstate_ls, cstatus_ls):
    state_pair.setdefault(k, []).append(v)    
state_pair

# Compute count
cert_count_s = [] 
for i in range(len(state_pair.keys())):
    sequence_of_status = list(state_pair.values())[i]
    counts = Counter()
    for certified in sequence_of_status:
       counts.update(word.strip('.,?!"\'- ').lower() for word in certified.split())       
    cert_count_s.append(counts['certified'])

# Compute percentage
totalcert_s = sum(cert_count_s)
percent_cert_s = [x * 100 / totalcert_s for x in cert_count_s]

percent_cert_s = [float(Decimal("%.1f" % e)) for e in percent_cert_s]
percent_cert_s = list(map("{}%".format, percent_cert_s))

state_list = state_pair.keys()

cert_count_s, state_list, percent_cert_s = zip(*sorted(zip(cert_count_s, state_list, percent_cert_s), reverse=True))
cert_count_s = list(cert_count_s)
state_list = list(state_list)
percent_cert_s = list(percent_cert_s)

# Compile the top 10 States, their counts, and percent by order.
topstate = init_list_of_objects(3)
if len(state_list) >=10:
   topstate[0] = state_list[0:10]
   topstate[1] = cert_count_s[0:10]
   topstate[2] = percent_cert_s[0:10]
else:
   length_sl = len(state_list)
   topstate[0] = state_list[0:length_sl]
   topstate[1] = cert_count_s[0:length_sl]
   topstate[2] = percent_cert_s[0:length_sl]
   if len(set(topstate[1]))< len(topstate[1]):
       m = topstate[1]
       m = list(set([x for x in m if m.count(x) > 1]))
       for i in m:
           position = [index for index, value in enumerate(topstate[1]) if value == i]
           topstate[0][position[0]:position[-1]+1] = sorted(topstate[0][position[0]:position[-1]+1])
           topstate[2][position[0]:position[-1]+1] = sorted(topstate[2][position[0]:position[-1]+1])
topstate[1] = [str(itm) for itm in topstate[1]]
       

topstate = list(zip(topstate[0], topstate[1], topstate[2]))
topstate.insert(0, ['TOP_STATES', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE'])
topstate = [list(i) for i in topstate]


for i in range(len(topstate)):
    topstate[i] = ';'.join(topstate[i])

# Write a new text file into output folder
with open(top_10_states_path, 'w') as f:
    for item in topstate:
        f.write("%s\n" % item)






#sample = init_list_of_objects(3)
#sample[0] = ['A','C','B','D','H','G','F','J']
#sample[1] = [20,10,10,5,2,2,2,1]
#sample[2] = [2,1,1,0.5,0.2,0.2,0.2,0.1]


#l = sample[1]
#l = list(set([x for x in l if l.count(x) > 1]))
#for i in l:
#    position = [index for index, value in enumerate(sample[1]) if value == i]
#    sample[0][position[0]:position[-1]+1] = sorted(sample[0][position[0]:position[-1]+1])
#    sample[2][position[0]:position[-1]+1] = sorted(sample[2][position[0]:position[-1]+1])

    




