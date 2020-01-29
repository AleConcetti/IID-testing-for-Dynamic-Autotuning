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

#%%
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Generate universe variables
#   * Quality and service on subjective ranges [0, 10]
#   * Tip has a range of [0, 25] in units of percentage points
x_qual = np.arange(0, 11, 1)
x_serv = np.arange(0, 11, 1)
x_tip  = np.arange(0, 26, 1)

# Generate fuzzy membership functions
qual_lo = fuzz.trimf(x_qual, [0, 0, 5])
qual_md = fuzz.trimf(x_qual, [0, 5, 10])
qual_hi = fuzz.trimf(x_qual, [5, 10, 10])
serv_lo = fuzz.trimf(x_serv, [0, 0, 5])
serv_md = fuzz.trimf(x_serv, [0, 5, 10])
serv_hi = fuzz.trimf(x_serv, [5, 10, 10])
tip_lo = fuzz.trimf(x_tip, [0, 0, 13])
tip_md = fuzz.trimf(x_tip, [0, 13, 25])
tip_hi = fuzz.trimf(x_tip, [13, 25, 25])

# Visualize these universes and membership functions
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

ax0.plot(x_qual, qual_lo, 'b', linewidth=1.5, label='Bad')
ax0.plot(x_qual, qual_md, 'g', linewidth=1.5, label='Decent')
ax0.plot(x_qual, qual_hi, 'r', linewidth=1.5, label='Great')
ax0.set_title('Food quality')
ax0.legend()

ax1.plot(x_serv, serv_lo, 'b', linewidth=1.5, label='Poor')
ax1.plot(x_serv, serv_md, 'g', linewidth=1.5, label='Acceptable')
ax1.plot(x_serv, serv_hi, 'r', linewidth=1.5, label='Amazing')
ax1.set_title('Service quality')
ax1.legend()

ax2.plot(x_tip, tip_lo, 'b', linewidth=1.5, label='Low')
ax2.plot(x_tip, tip_md, 'g', linewidth=1.5, label='Medium')
ax2.plot(x_tip, tip_hi, 'r', linewidth=1.5, label='High')
ax2.set_title('Tip amount')
ax2.legend()

# Turn off top/right axes
for ax in (ax0, ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()
#%%
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

x_qual = np.arange(0, 30, 1)

# Generate fuzzy membership functions
isIID = fuzz.trapmf(x_qual, [0,0,3, 15])
notIID = fuzz.trapmf(x_qual, [3, 15, 30, 30])

plt.title("Simulation Result")
blue_patch = mpatches.Patch(color='blue', label='isIID')
green_patch = mpatches.Patch(color='green', label='notIID')
#red_patch = mpatches.Patch(color='red', label='simulation result')
plt.legend(handles=[blue_patch,green_patch], loc=1)

plt.plot(x_qual, isIID, 'b', linewidth=1.5, label='Bad')
plt.plot(x_qual, notIID, 'g', linewidth=1.5, label='Decent')
plt.xlabel("Number of failed applications")
plt.ylabel("Membership percentage")
not_iid_counting=2
#plt.axvline(x=not_iid_counting,linewidth=1.5, color="red")
#print("isIID?", 1.0)
#print("notIID?", 0.0)
