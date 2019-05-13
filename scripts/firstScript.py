import os

#cmd = "gcc -I utilities -I linear-algebra/kernels/ utilities/polybench.c linear-algebra/kernels/atax/atax.c -o atax_base"

PATH_POLYBENCH = "benchmark/polybench-c-3.2/"
#os.system("cd "+PATH_POLYBENCH+"&& ls")


def funct(startpath,pippo):
    for root,dirs,files in os.walk(startpath):
        if (len(dirs)==0):
            for file in files:
                pippo =
                cmd = "gcc -I utilities -I linear-algebra/kernels/ utilities/polybench.c linear-algebra/kernels/atax/atax.c -o atax_base"
                os.sys(cmd)
                pass
        else:
            for dir in dirs:
                funct(startpath+"/"+dir)



def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        print(root,dirs, files)
        # level = root.replace(startpath, '').count(os.sep)
        # indent = ' ' * 4 * (level)
        # print('{}{}/'.format(indent, os.path.basename(root)))
        # subindent = ' ' * 4 * (level + 1)
        # for f in files:
        #     print('{}{}'.format(subindent, f))

funct(PATH_POLYBENCH)
