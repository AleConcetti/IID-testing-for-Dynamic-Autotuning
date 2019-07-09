from matplotlib import pyplot as plt
from scipy.stats import norm
from scipy.stats import ttest_ind
from scipy.stats import normaltest
from mlxtend.evaluate import permutation_test
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
    print(lim)
    print(len(data) - lim)
    for i in range(lim, len(data) - lim):
        sample = 0
        for j in range(FILTER_LEN):
            sample = sample + data[i + (j - lim)] * filter[j]
        clear_data.append(sample)
    print(clear_data)
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
def applyMask(array, mask, negation_mask=False):
    new_array=[]
    i=0
    for elem in array:
        if(not negation_mask):
            if(mask[i]):
                new_array.append(elem)
        else:
            if (not mask[i]):
                new_array.append(elem)

        i=i+1
    return new_array
def createFolds(dataset, k):
    indeces=[]
    for i in range(1,k):
        indeces.append(int(np.floor(len(dataset)* i / k)))
    return np.split(dataset, indeces)
def isIID_v1(dataset, alpha):
    data3, data4 = splitData(alternate=False, dataset = dataset)
    res = ttest_ind(data3, data4, equal_var=False)
    result=[]
    p = res.pvalue
    result.append(p > alpha)
    result.append(p)
    return result
def isIID_v2(dataset, alpha):
    fold1, fold2, fold3,fold4 = createFolds(dataset, 4)
    folds = [fold1, fold2, fold3, fold4]
    voteIID=0
    voteNotIID=0
    pvals=[]
    iid_list=[]
    for i in range(len(folds)):
        for j in range(i+1, len(folds)):
            res = ttest_ind(folds[i], folds[j], equal_var=False)
            pvals.append(res.pvalue)
            if(res.pvalue>alpha):
                voteIID=voteIID+1
                iid_list.append(True)
            else:
                voteNotIID=voteNotIID+1
                iid_list.append(False)

    if(voteIID>=voteNotIID):
        valid_pvalues = applyMask(pvals, iid_list)
        p_value = sum(valid_pvalues) / len(valid_pvalues)
        return [True, p_value]
    else:
        valid_pvalues = applyMask(pvals, iid_list, negation_mask=True)
        p_value = sum(valid_pvalues) / len(valid_pvalues)
        return [False, p_value]
def isIID_v3(dataset, alpha):
    voteIID = 0
    voteNotIID = 0
    pvals = []
    iid_list=[]

    fold1, fold2, fold3, fold4, fold5 = createFolds(dataset,5)
    folds = [fold1, fold2, fold3, fold4, fold5]
    for i in range(len(folds)):
        folds_temp = folds.copy()
        fold_test = folds_temp.pop(i)
        oof = [i for fold in folds_temp for i in fold]
        #res = ttest_ind(fold_test, oof, equal_var=False)
        # http://rasbt.github.io/mlxtend/user_guide/evaluate/permutation_test/
        p = permutation_test(fold_test, oof, method='approximate', seed=0 )
        pvals.append(p)
        if (p > alpha):
            voteIID = voteIID + 1
            iid_list.append(True)
        else:
            voteNotIID = voteNotIID + 1
            iid_list.append(False)

    if (voteIID >= voteNotIID):
        valid_pvalues =  applyMask(pvals, iid_list)
        p_value=sum(valid_pvalues)/len(valid_pvalues)
        return [True, p_value]
    else:
        valid_pvalues = applyMask(pvals, iid_list, negation_mask=True)
        p_value = sum(valid_pvalues) / len(valid_pvalues)
        return [False, p_value]
def isGaussian(dataset, alpha):
    stats, p = normaltest(dataset)
    return p>alpha


SIMS ={4: "sim4_vergine",
       5: "sim5_with_DVFS",
       6: "sim6_with_shared_cache",
       7: "sim7_with_system_noise",
       8: "sim8_with_turbo",
       9: "sim9_system_noise_and_shared_cache",
       10:"sim10_with_corunning_apps"
       }

SIM=SIMS.get(4)
PATH="../../workingFiles/simulation_data/"+SIM+"/execution_times/"
NUM_OF_BIN=30
FILTER_LEN=21
name_of_files=readNameOfFiles()
#name_of_files=['execution_times_covariance.csv', 'execution_times_2mm.csv', 'execution_times_durbin.csv','execution_times_gemm.csv', 'execution_times_symm.csv','execution_times_syrk.csv']
i=0
j = 0
for NAME_OF_FILE in name_of_files:
    NAME_OF_PROGRAM = NAME_OF_FILE.replace("execution_times_","").replace(".csv","")

    data = readDataFromFile(open(PATH + NAME_OF_FILE))
    #data=deleteOutlier(data_withOutlier)
    #print(NAME_OF_FILE)
    #print(isGaussian(data, 0.05))
    #if(not isGaussian(data, 0.05)):
    #    j=j+1
    #    print(i)

    alpha=0.05
    res = isIID_v3(data, alpha)
    is_iid = res[0]
    p = res[1]
    result_of_test="IID with p-value "+str(round(p,10))
    if not is_iid:
        print("[", NAME_OF_PROGRAM, "]", "p-value: " + str(round(p,10)), "IID: " + str(is_iid))
        result_of_test= "NOT "+result_of_test


    plt.figure(1, figsize=(20,5))
    plt.suptitle(NAME_OF_PROGRAM.upper()+" ("+result_of_test+")", size=20)

    plt.subplot(121)
    plt.title("Data occurrence")
    plt.hist(data, NUM_OF_BIN)
    plt.xlabel("Execution times [seconds]")

    #plt.subplot(132)
    #plt.title("Data Density vs Gaussian")
    #plt.hist(data, NUM_OF_BIN, density=True)
    #min_lim= min(data) - (max(data) - min(data)) / 4
    #max_lim= max(data) + (max(data) - min(data)) / 4
    #plt.xlim((min_lim, max_lim))
    #x = np.linspace(min_lim, max_lim, 100)
    #plt.plot(x, norm.pdf(x, np.mean(data), np.sqrt(np.var(data, ddof=1))))
    #plt.xlabel("Execution times [seconds]")

    plt.subplot(122)
    plt.title("Execution times")
    x = np.linspace(0, len(data), len(data))
    plt.plot(x, data, color="GRAY")
    plt.plot(x, data, color="LIGHTGREEN")
    plt.xlabel("Simulations")

    clear_data=conv1D(FILTER_LEN, data)
    plt.plot(x,clear_data,color="RED")
    i=i+1
    gray_patch = mpatches.Patch(color='GRAY', label='data')
    green_patch = mpatches.Patch(color='LIGHTGREEN', label='data with no outlier')
    red_patch = mpatches.Patch(color='RED', label='data mean')
    plt.legend(handles=[gray_patch,green_patch,red_patch], loc=1)
    plt.savefig("pdfs/"+NAME_OF_PROGRAM+".pdf")
    plt.close()


os.system("pdftk pdfs/*.pdf cat output "+SIM+".pdf")
os.system("cd pdfs && ls | grep -v "+SIM+".pdf | xargs rm")
