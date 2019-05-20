import os

#cmd = "gcc -I utilities -I linear-algebra/kernels/ utilities/polybench.c linear-algebra/kernels/atax/atax.c -o atax_base"

PATH_POLYBENCH = "benchmark/polybench-c-3.2/utilities"
#os.system("cd "+PATH_POLYBENCH+"&& ls")


f=open(PATH_POLYBENCH+"/benchmark_list","r")
f1 = f.readlines()

# build code and path
i=0
codesList=[]
nameList=[]
pathList=[]
commandList=[]

for x in f1:
    #print("code:")
    codesList.append(x[2:len(x)])
    #print(codesList[0])
    i=-1
    temp = list(codesList[0])
    tempName=[]
    while(temp[i]!='/'):
        if(i<-3):
            tempName.append(temp[i])
        temp[i]= ''
        i-=1
    tempName.reverse
    path= "".join(temp)
    pathList.append(path)
    name="".join(reversed(tempName))
    nameList.append(name)
    #print("path:")
    #print(path)
    #print("name:")
    #print(name)
    i+=1

for i in range(len(pathList)):
    cmd="gcc -I utilities -I "+pathList[i]+"utilities/polybench.c "+codesList[i]+"-o "+nameList[i]+"_base"
    print(cmd)
    commandList.append(cmd)
