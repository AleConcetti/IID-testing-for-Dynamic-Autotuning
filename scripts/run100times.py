# gcc -O3 -I utilities -I linear-algebra/kernels/atax utilities/polybench.c linear-algebra/kernels/atax/atax.c -DPOLYBENCH_TIME -o atax_time

import csv
import os
import numpy as np

NUM_OF_EXECUTIONS=10
os.system(">execution_times.csv")
os.system("clear")
execution_times=[];
os.system("gcc -O3 -I utilities -I linear-algebra/kernels/atax utilities/polybench.c linear-algebra/kernels/atax/atax.c -DPOLYBENCH_TIME -o atax_time")

for i in range(NUM_OF_EXECUTIONS):
    os.system("clear")
    print(str(100*(i/NUM_OF_EXECUTIONS))+"%"+" "+"|"*i)
    os.system("./atax_time >> execution_times.csv")
os.system("clear")
print("100%"+"|"*100)
os.system("rm atax_time");

with open("execution_times.csv") as f:
    reader = csv.reader(f)
    ex_times = []
    for row in reader:
        ex_times.append(float(list(row)[0]))

print("Average Execution Time: "+str(np.average(ex_times)))
print("Variance Execution Time: "+str(np.var(ex_times,ddof=1)))
