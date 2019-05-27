import matplotlib.pyplot as plt
import csv

f=open("prova.csv", "r")
reader=csv.reader(f)
data=[]
for raw in reader:
    if "~~~~~" in str(raw):
        break;
    for value in raw:
        data.append(float(value))
f.close()
print(data)
plt.hist(data, 25)
plt.show()