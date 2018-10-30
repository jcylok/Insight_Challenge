import sys
import csv
from collections import Counter
from decimal import Decimal

[input_file, top_10_occupation_path, top_10_states_path] = sys.argv[1:] #assign paths

with open(input_file) as csv_file: #read input file and break the rows
    reader = csv.reader(csv_file, delimiter=";", strict=False)
    result = []
    for row in reader:
        if row == []:
            break
        result += [row]

def init_list(size): #define a new function that creates a list of lists
    list_of_objects = list()
    for i in range(0,size):
        list_of_objects.append(list())
    return list_of_objects

        
keys = result[0] #extraxt column names
keys = [k.upper() for k in keys] #convert to capital letters for consistency
a = init_list(len(keys))     
for i in range(len(keys)): #re-arrange all entry data by columns' order
    for j in range(1, len(result)):
        a[i].append(result[j][i])   
        
dicts = {} #create a dictionary where keys are the column names and values are the corresponding entry data
values = a
for i in range(len(keys)):
    dicts[keys[i]] = values[i]
    
##### Top 10 Occupations #####

# Extract needed keys and values from raw data
socname = [s for s in keys if "SOC" in s and "NAME" in s]  #find key associated with SOC Name
socname = next(iter(socname))

cstatus = [c for c in keys if "STATUS" in c] #find key associated with Case Status
cstatus = next(iter(cstatus))

socname_ls = [k.upper() for k in dicts[socname]] #convert all characters to capital letters
cstatus_ls = [k.upper() for k in dicts[cstatus]]

occ_pair = {}
for k, v in zip(socname_ls, cstatus_ls): #pair up each occupation with their list of case status
   occ_pair.setdefault(k, []).append(v)    

# Compute count of 'certified' cases for each occupation
cert_count = [] 
for i in range(len(occ_pair.keys())):
    sequence_of_status = list(occ_pair.values())[i]
    counts = Counter()
    for certified in sequence_of_status:
       counts.update(word.strip('.,?!"\'- ').lower() for word in certified.split())       
    cert_count.append(counts['certified'])

# Compute percentage of 'certified' cases for each occupation
totalcert = sum(cert_count)
percent_cert = [x * 100 / totalcert for x in cert_count]
percent_cert = [float(Decimal("%.1f" % e)) for e in percent_cert]
percent_cert = list(map("{}%".format, percent_cert))

occ_list = occ_pair.keys()

cert_count, occ_list, percent_cert = zip(*sorted(zip(cert_count, occ_list, percent_cert), reverse=True))
cert_count = list(cert_count)
occ_list = list(occ_list)
percent_cert = list(percent_cert)

# Compile top 10 occupations, their counts, and percentages by order.
topocc = init_list(3)
if len(occ_list) >=10:
   topocc[0] = occ_list[0:10]
   topocc[1] = cert_count[0:10]
   topocc[2] = percent_cert[0:10]
else:   #this condition is for cases where top occupations are smaller than 10
   length = len(occ_list)
   topocc[0] = occ_list[0:length]
   topocc[1] = cert_count[0:length]
   topocc[2] = percent_cert[0:length]
   if len(set(topocc[1]))< len(topocc[1]): #in case of a tie, order alphabetically by TOP_OCCUPATIONS
       l = topocc[1]
       l = list(set([x for x in l if l.count(x) > 1]))
       for i in l:
           position = [index for index, value in enumerate(topocc[1]) if value == i]
           topocc[0][position[0]:position[-1]+1] = sorted(topocc[0][position[0]:position[-1]+1])
           topocc[2][position[0]:position[-1]+1] = sorted(topocc[2][position[0]:position[-1]+1])
topocc[1] = [str(itm) for itm in topocc[1]]
       

topocc = list(zip(topocc[0], topocc[1], topocc[2]))
topocc.insert(0, ['TOP_OCCUPATIONS', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE']) #insert column names
topocc = [list(i) for i in topocc]

for i in range(len(topocc)): #add semicolons
    topocc[i] = ';'.join(topocc[i])

# Write a new text file into output folder
with open(top_10_occupation_path, 'w') as f:
    for item in topocc:
        f.write("%s\n" % item)


##### Top 10 States #####
        
# Extract needed keys and values from raw data
workstate = [s for s in keys if "WORK" in s and "STATE" in s]  #find key associated with states where the work take place
workstate = next(iter(workstate))
workstate_ls = [k.upper() for k in dicts[workstate]] #convert all characters to capital letters

state_pair = {}
for k, v in zip(workstate_ls, cstatus_ls): #pair up each state with their list of case status
    state_pair.setdefault(k, []).append(v)

# Compute count of 'certified' cases for each state
cert_count_s = [] 
for i in range(len(state_pair.keys())):
    sequence_of_status = list(state_pair.values())[i]
    counts = Counter()
    for certified in sequence_of_status:
       counts.update(word.strip('.,?!"\'- ').lower() for word in certified.split())       
    cert_count_s.append(counts['certified'])

# Compute percentage of 'certified' cases for each state
totalcert_s = sum(cert_count_s)
percent_cert_s = [x * 100 / totalcert_s for x in cert_count_s]

percent_cert_s = [float(Decimal("%.1f" % e)) for e in percent_cert_s]
percent_cert_s = list(map("{}%".format, percent_cert_s))

state_list = state_pair.keys()

cert_count_s, state_list, percent_cert_s = zip(*sorted(zip(cert_count_s, state_list, percent_cert_s), reverse=True))
cert_count_s = list(cert_count_s)
state_list = list(state_list)
percent_cert_s = list(percent_cert_s)

# Compile top 10 states, their counts, and percentages by order.
topstate = init_list(3)
if len(state_list) >= 10:
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
       m = list(set([x for x in m if m.count(x) > 1])) #in case of a tie, order alphabetically by TOP_STATES
       for i in m:
           position = [index for index, value in enumerate(topstate[1]) if value == i]
           topstate[0][position[0]:position[-1]+1] = sorted(topstate[0][position[0]:position[-1]+1])
           topstate[2][position[0]:position[-1]+1] = sorted(topstate[2][position[0]:position[-1]+1])
topstate[1] = [str(itm) for itm in topstate[1]]
       

topstate = list(zip(topstate[0], topstate[1], topstate[2]))
topstate.insert(0, ['TOP_STATES', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE']) #insert column names
topstate = [list(i) for i in topstate]


for i in range(len(topstate)): #add semicolons
    topstate[i] = ';'.join(topstate[i])

# Write a new text file into output folder
with open(top_10_states_path, 'w') as f:
    for item in topstate:
        f.write("%s\n" % item)
