import os

# gcc -O3 -I utilities -I linear-algebra/kernels/atax utilities/polybench.c linear-algebra/kernels/atax/atax.c -DPOLYBENCH_TIME -o atax_time
PATH_POLYBENCH = "../benchmark/polybench-c-3.2/"
#os.system("cd "+PATH_POLYBENCH+"&& ls")



def funct(startpath,pippo):
    for root,dirs,files in os.walk(startpath):
        if (len(dirs)==0):
            for file in files:
                cmd = "gcc -I utilities -I linear-algebra/kernels/ utilities/polybench.c linear-algebra/kernels/atax/atax.c -o atax_base"
                os.sys(cmd)
                pass
        else:
            for dir in dirs:
                funct(startpath+"/"+dir)
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        print(root,dirs, files)


list_files(PATH_POLYBENCH)
