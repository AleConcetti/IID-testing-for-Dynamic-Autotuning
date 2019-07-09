#%%
from matplotlib import pyplot as plt
from scipy.stats import norm
from scipy.stats import ttest_ind
from scipy.stats import normaltest
from mlxtend.evaluate import permutation_test
import numpy as np
import matplotlib.patches as mpatches
import os

# Function definition
def readNameOfFiles():
    f=open("name_of_files.txt") # generato con ls
    name_of_files=[]
    for raw in f:
        if ".csv" in str(raw):
            name_of_files.append(str(raw).replace("\n",""))
    f.close()
    return name_of_files

def readDataFromFile(f):
    data = []
    for raw in f:
        if "~~~~" in raw:
            break
        data.append(float(raw))
    return data

def deleteOutlier(data):
    mean_data = np.mean(data)
    dev_stand_data = np.sqrt(np.var(data, ddof=1))
    max_lim = mean_data + 2*dev_stand_data
    min_lim = mean_data - 2*dev_stand_data

    clear_data=[]
    for i in range(len(data)):
        if(min_lim<data[i] and data[i]<max_lim):
            clear_data.append(data[i])
        else:
            clear_data.append(mean_data)

    return clear_data

# Variable definition
SIMS ={4: "sim4_vergine",
       5: "sim5_with_DVFS",
       6: "sim6_with_shared_cache",
       7: "sim7_with_system_noise",
       8: "sim8_with_turbo",
       9: "sim9_system_noise_and_shared_cache"
       }

SIM=SIMS.get(4)
PATH="../../workingFiles/simulation_data/"+SIM+"/execution_times/"
NUM_OF_BIN=30
FILTER_LEN=21
name_of_files=readNameOfFiles()

#%%
NAME_OF_FILE = name_of_files[2] 
NAME_OF_PROGRAM = NAME_OF_FILE.replace("execution_times_","").replace(".csv","")
data_withOutlier = readDataFromFile(open(PATH + NAME_OF_FILE))
data=deleteOutlier(data_withOutlier)

plt.title("Data Density")
plt.hist(data, NUM_OF_BIN, density=True)
plt.xlabel("Execution times [seconds]")

#%%
#print(data)
plt.title("Data Density")
#plt.hist([np.exp(data) for i in data], NUM_OF_BIN, density=True)
plt.hist([np.exp(1)**(-30*i) for i in data], NUM_OF_BIN, density=True)
plt.xlabel("Execution times [seconds]")
