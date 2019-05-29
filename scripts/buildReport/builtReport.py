from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import norm
import os
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

def conv1D(FILTER_LEN):
    filter = np.ones(FILTER_LEN) / FILTER_LEN
    lim = int(np.floor(FILTER_LEN / 2))
    clear_data = []
    for i in range(lim, len(data) - lim):
        sample = 0
        for j in range(FILTER_LEN):
            sample = sample + data[i + (j - lim)] * filter[j]
        clear_data.append(sample)
    return list(np.ones(lim)*clear_data[0])+clear_data+list(np.ones(lim)*clear_data[-1])

SIM="sim0"
PATH="../../workingFiles/simulation_data/"+SIM+"/execution_times/"
NUM_OF_BIN=7
FILTER_LEN=3
name_of_files=readNameOfFiles()
i=0
for NAME_OF_FILE in name_of_files:
    #NAME_OF_FILE = name_of_files[0]
    NAME_OF_PROGRAM = NAME_OF_FILE.replace("execution_times_","").replace(".csv","")

    data=readDataFromFile(open(PATH+NAME_OF_FILE))

    plt.figure(1, figsize=(15,5))
    plt.suptitle(NAME_OF_PROGRAM)
    plt.subplot(121)
    plt.hist(data, NUM_OF_BIN, density=True)
    min_lim= min(data) - (max(data) - min(data)) / 2
    max_lim= max(data) + (max(data) - min(data)) / 2
    plt.xlim((min_lim, max_lim))
    x = np.linspace(min_lim, max_lim, 100)
    plt.plot(x,norm.pdf(x,np.mean(data),np.sqrt(np.var(data, ddof=1))))

    plt.subplot(122)
    x = np.linspace(0, len(data), len(data))
    plt.plot(x,data,color="GRAY")

    clear_data=conv1D(FILTER_LEN)
    plt.plot(x,clear_data,color="RED")
    plt.savefig("pdfs/"+str(i)+"_"+NAME_OF_PROGRAM+".pdf")
    i=i+1
    plt.close()

os.system("pdftk pdfs/*.pdf cat output "+SIM+".pdf")
os.system("cd pdfs && ls | grep -v "+SIM+".pdf | xargs rm")