from matplotlib import pyplot as plt
from scipy.stats import norm
from scipy.stats import ttest_ind
import numpy as np
import matplotlib.patches as mpatches
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
def conv1D(FILTER_LEN, data):
    filter = np.ones(FILTER_LEN) / FILTER_LEN
    lim = int(np.floor(FILTER_LEN / 2))
    clear_data = []
    for i in range(lim, len(data) - lim):
        sample = 0
        for j in range(FILTER_LEN):
            sample = sample + data[i + (j - lim)] * filter[j]
        clear_data.append(sample)
    return list(np.ones(lim)*clear_data[0])+clear_data+list(np.ones(lim)*clear_data[-1])
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
def splitData(dataset, alternate=False):

    if(not alternate):
        split_index = int(np.floor(len(dataset) / 2))
        data3 = dataset[:split_index]
        data4 = dataset[split_index:]
        return data3, data4
    else:
        data1 = [dataset[i] for i in range(len(dataset)) if i % 2 == 0]
        data2 = [dataset[i] for i in range(len(dataset)) if i % 2 == 1]
        return data1, data2


SIM="sim6"
PATH="../../workingFiles/simulation_data/"+SIM+"/execution_times/"
NUM_OF_BIN=30
FILTER_LEN=21
name_of_files=readNameOfFiles()
#name_of_files=['execution_times_covariance.csv', 'execution_times_2mm.csv', 'execution_times_durbin.csv','execution_times_gemm.csv', 'execution_times_symm.csv','execution_times_syrk.csv']
i=0
for NAME_OF_FILE in name_of_files:
    NAME_OF_PROGRAM = NAME_OF_FILE.replace("execution_times_","").replace(".csv","")

    data_withOutlier=readDataFromFile(open(PATH + NAME_OF_FILE))
    data=deleteOutlier(data_withOutlier)

    data3, data4 = splitData(alternate=False, dataset= data)
    res = ttest_ind(data3, data4, equal_var=False)
    p = res.pvalue
    alpha = 0.05
    isIID = p > alpha
    result_of_test="IID with p-value "+str(round(p,10))
    if not isIID:
        print("[", NAME_OF_PROGRAM, "]", "p-value: " + str(round(p, 10)), "IID: " + str(isIID))
        result_of_test= "NOT "+result_of_test

    plt.figure(1, figsize=(20,5))
    plt.suptitle(NAME_OF_PROGRAM.upper()+" ("+result_of_test+")", size=20)

    plt.subplot(131)
    plt.title("Data occurrence")
    plt.hist(data, NUM_OF_BIN)

    plt.subplot(132)
    plt.title("Data Density vs Gaussian")
    plt.hist(data, NUM_OF_BIN, density=True)
    min_lim= min(data) - (max(data) - min(data)) / 4
    max_lim= max(data) + (max(data) - min(data)) / 4
    plt.xlim((min_lim, max_lim))
    x = np.linspace(min_lim, max_lim, 100)
    plt.plot(x, norm.pdf(x, np.mean(data), np.sqrt(np.var(data, ddof=1))))

    plt.subplot(133)
    plt.title("Execution times")
    x = np.linspace(0, len(data_withOutlier), len(data_withOutlier))
    plt.plot(x, data_withOutlier, color="GRAY")
    plt.plot(x, data, color="LIGHTGREEN")

    clear_data=conv1D(FILTER_LEN, data_withOutlier)
    plt.plot(x,clear_data,color="RED")
    i=i+1
    gray_patch = mpatches.Patch(color='GRAY', label='data')
    green_patch = mpatches.Patch(color='LIGHTGREEN', label='data with no outlier')
    red_patch = mpatches.Patch(color='RED', label='data mean')
    plt.legend(handles=[gray_patch,green_patch,red_patch], loc=1)
    plt.savefig("pdfs/"+str(i)+"_"+NAME_OF_PROGRAM+".pdf")
    plt.close()





os.system("pdftk pdfs/*.pdf cat output "+SIM+".pdf")
os.system("cd pdfs && ls | grep -v "+SIM+".pdf | xargs rm")
