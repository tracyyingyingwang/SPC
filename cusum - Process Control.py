import time
import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import math
import statistics
import numpy
from itertools import *

df = pd.read_csv("GB_Baseline.csv", na_filter=False)
df = df[["Input_Roller_Bearing", "Output_Roller_Bearing"]]
data_train = df['Input_Roller_Bearing']

df1 = pd.read_csv("GB_TempFault.csv", na_filter=False)
df1 = df1[["Input_Roller_Bearing", "Output_Roller_Bearing"]]
data_test = df1['Input_Roller_Bearing']

meanVal = []
consecutive = []

def meanLister(data):
    i = 1
    consecutiveList = []
    meanVal = []
    for i in range(len(data)):
        consecutive.append(abs(data[i]))
        if len(consecutive) == 5:
            Mean = sum(consecutive) / len(consecutive)
            meanVal.append(Mean)
            consecutive.clear()
        i == i+1
    return meanVal

means = meanLister(data_train)
means_faulty = meanLister(data_test)
targetMean = sum(means)/len(means)
targetStdev = statistics.stdev(means)
faultyMean = sum(means_faulty)/len(means_faulty)
k_norm = abs(targetMean-targetMean)/2   # reference value
k_faulty = abs(faultyMean-targetMean)/2   # reference value
h = 5*targetStdev   # decision interval

ci_plus, ci_minus, N_plus, N_minus = ([0], [0], [0], [0])
i = 1
for item in means:
    ci_plus.append(max(0,item-targetMean-k_norm+ci_plus[i-1]))
    ci_minus.append(max(0, targetMean-k_norm-item+ci_minus[i-1]))
    if ci_plus[i]>0:
        N_plus.append(N_plus[i-1]+1)
    else:
        N_plus.append(0)
    if ci_minus[i]>0:
        N_minus.append(N_minus[i-1]+1)
    else:
        N_minus.append(0)

    i += 1
negCi_minus = [-x for x in ci_minus]
del ci_plus[0]
del negCi_minus[0]

ci_plus1, ci_minus1 = ([ci_plus[-1]], [ci_minus[-1]])
i = 1
for item in means_faulty:
    ci_plus1.append(max(0,item-targetMean-k_faulty+ci_plus1[i-1]))
    ci_minus1.append(max(0, targetMean-k_faulty-item+ci_plus1[i-1]))
    i += 1
negCi_minus1 = [-x for x in ci_minus1]
del ci_plus1[0]
del negCi_minus1[0]

'''
ciPlus = []
ciMinus = []
for i in chain(negCi_minus, negCi_minus1):
    ciMinus.append(i)
for i in chain(ci_plus, ci_plus1):
    ciPlus.append(i)
'''

#y = [list(a) for a in zip(ciPlus, ciMinus)]
y = [list(a) for a in zip(ci_plus1, negCi_minus1)]
x = range(0, len(y))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
markers = ["o", "i"]

for xe, ye in zip(x, y):
    if y[xe][0] > h:
        colors = 'r'
    else:
        colors = 'k'
    if y[xe][1] < -h:
        colors1 = 'r'
    else:
        colors1 = 'xkcd:grey'
    plt.scatter([xe] * len(ye), ye, marker='o', s=10, color=[colors, colors1])

plt.xlim(0, 20)
y_min, y_max = ax.get_ylim()
x_min, x_max = ax.get_xlim()

plt.xlabel('Time (s)')
plt.ylabel('F2')
plt.title('F2 vs. Time')
plt.axhline(y=h, xmin=0, xmax=1, linewidth=1.5, color='orange')
plt.axhline(y=-h, xmin=0, xmax=1, linewidth=1.5, color='orange')
#plt.axvline(x=120, ymin=-0, ymax=1, linewidth=1, color='xkcd:grey')
plt.annotate('+H', weight='bold', color='orange', xy=(2, h+0.2))
plt.annotate('- H', weight='bold', color='orange', xy=(2, -h-0.4))
#ax.axvspan(120, 240, alpha=0.2, color='grey')
plt.grid()
plt.axhline(y=0, xmin=0, xmax=1, linewidth=1, color='xkcd:grey')
plt.show()