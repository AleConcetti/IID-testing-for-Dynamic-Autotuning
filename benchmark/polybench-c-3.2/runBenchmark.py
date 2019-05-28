import time
import os
import csv
import numpy as np
from subprocess import PIPE, call
def prepocessing():
    PATH_POLYBENCH = "utilities"
    f=open(PATH_POLYBENCH+"/benchmark_list","r")
    f1 = f.readlines()

    # build code and path
    i=0
    codesList=[]
    nameList=[]
    pathList=[]
    commandList=[]

    for x in f1:
        codesList.append(x[2:len(x)])
        i=-1
        temp = list(codesList[i])
        tempName=[]
        while(temp[i]!='/'):
            if(i<-3):
                tempName.append(temp[i])
            temp[i]= ''
            i-=1
        path= "".join(temp)
        pathList.append(path)
        name="".join(reversed(tempName))
        nameList.append(name)
        i+=1

    for i in range(len(pathList)):
        cmd="gcc -O3 -I utilities -I "+pathList[i]+" utilities/polybench.c "+codesList[i].replace("\n"," ")+"-DPOLYBENCH_TIME -o "+nameList[i]+"_time -lm"
        #print(cmd)
        commandList.append(cmd)
    return commandList,nameList
def processing(NUM_OF_EXECUTION, commandList, nameList):
    ex_times_list = []
    for i in range(0, len(commandList)):
        cmd = commandList[i]
        name_of_script = nameList[i]
        outFileName = "execution_times_" + name_of_script + ".csv"

        call(">execution_times_" + name_of_script + ".csv", shell=True)
        # Clean up the caches
        os.system("sync; echo 3 > /proc/sys/vm/drop_caches")
        call(cmd, shell=True)

        while name_of_script + "_time" not in os.listdir("."):
            time.sleep(1)

        print("Program ", i, "/", len(commandList), ": ", name_of_script.upper(), sep="")
        for j in range(NUM_OF_EXECUTIONS):
            print("Execution ", j + 1, "/", NUM_OF_EXECUTIONS, sep="")
            call("./" + name_of_script + "_time >> " + outFileName, shell=True, stdout=PIPE)

        print("Finish!\n")
        print("-" * 20, "\n")
        call(("rm " + name_of_script + "_time"), shell=True)

        ex_times = []
        with open("execution_times_" + name_of_script + ".csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                ex_times.append(float(list(row)[0]))
            f.close()
        ex_times_list.append(ex_times)

        with open("execution_times_" + name_of_script + ".csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(["~" * 50])
            writer.writerow(["Avg ExTime: " + str(np.average(ex_times))])
            writer.writerow(["Var ExTime: " + str(np.var(ex_times, ddof=1))])
            f.close()

    return ex_times_list
def printReportSimulation(ex_times_list, start,end_preprocessing, end):
    approx=4
    print("Tot time:",round(end-start, approx))
    time_preprocessing=round(end_preprocessing-start, approx)
    print("Time preprocessing:",time_preprocessing)
    time_processing=round(end-end_preprocessing,approx)
    print("Time for processing:", time_processing)
    sum=0
    for ex_times in ex_times_list:
        for ex_time in ex_times:
            sum = sum + ex_time
    print("\tof which", round(time_processing-sum, approx), "is overhead")

#----------------------START----------------------
start = time.time()

NUM_OF_EXECUTIONS=200

#----------------------PREPROCESSING----------------------
commandList, nameList = prepocessing()
end_preprocessing = time.time();

#----------------------PROCESSING----------------------
ex_times_list = processing(NUM_OF_EXECUTIONS,commandList,nameList)

end = time.time()

#----------------------PRINT REPORT----------------------
printReportSimulation(ex_times_list,start, end_preprocessing,end)