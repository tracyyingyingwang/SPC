import time
import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import math
import statistics
import numpy

#df = pd.read_csv("C:/Users/Jared O'Quinn/Desktop/anil/Statistical Process Control/Python/Shewhart Control Chart/Normal_DE_Casing.csv", na_filter=False)
df = pd.read_csv("C:/Users/Jared O'Quinn/Desktop/anil/Statistical Process Control/Python/Shewhart Control Chart/ProcessControlNormal1.csv", na_filter=False)
#df = pd.read_csv("C:/Users/Jared O'Quinn/Desktop/anil/Statistical Process Control/Python/Shewhart Control Chart/Clint.csv", na_filter=False)
df = df[["time", "P1"]]

data_train = df['P1']

#df1 = pd.read_csv("C:/Users/Jared O'Quinn/Desktop/anil/Statistical Process Control/Python/Shewhart Control Chart/Cavitation_DE_Casing.csv", na_filter=False)
df1 = pd.read_csv("C:/Users/Jared O'Quinn/Desktop/anil/Statistical Process Control/Python/Shewhart Control Chart/ProcessControlFaulty1.csv", na_filter=False)
df1 = df1[["time", 'P1']]

data_test = df1['P1']

x_bar = []
s = []
consecutive = []

sample_size = 1000
sample_size_test = 1000

stop = len(data_train)
stop_test = len(data_test)

i = 0
for i in range(len(data_train)):
    consecutive.append(data_train[i])
    if len(consecutive) == sample_size:
        mean = sum(consecutive)/len(consecutive)
        x_bar.append(mean)
        sigma = statistics.stdev(consecutive)
        s.append(sigma)
        consecutive.clear()
    if i == stop:
        break

sbar = sum(s)/len(s)
xbar_bar = sum(x_bar)/len(x_bar)
c4 = (4*(sample_size-1))/((4*sample_size)-3)
B3 = 1 - ((3/c4)*(math.sqrt(1-c4**2)))
B4 = 1 + ((3/c4)*(math.sqrt(1-c4**2)))
ucl = sbar * B4
lcl = sbar * B3

consecutive2 = []
s_plot = {}

i = 0
k = 1
for i in range(len(data_test)):
    consecutive2.append(data_test[i])
    if len(consecutive2) == sample_size_test:
        sigma1 = statistics.stdev(consecutive2)
        # mean_plot[dt.datetime.now().strftime('%H:%M:%S')] = mean
        s_plot[k] = sigma1
        k += 1
        consecutive2.clear()
        # time.sleep(0.90)
    if i == stop_test:
        break

import matplotlib.pylab as plt

lists = sorted(s_plot.items()) # sorted by key, return a list of tuples
x, y = zip(*lists) # unpack a list of pairs into two tuples

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

for i in range(len(s_plot)):
    if y[i] > ucl or y[i] < lcl: # rule 1: if any point is outside of the control limits color it red
        colors = 'r'
    else:
        colors = 'b'
    ax.scatter(x[i], y[i], color=colors)

# plt.plot(x, y, '-o', color)

plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.30)
plt.title('Vibration vs. Time')
plt.ylabel('Motor DE Vibration')
plt.axhline(y=sbar, xmin=0, xmax=1, linewidth=2, color = 'k')
plt.axhline(y=ucl, xmin=0, xmax=1, linewidth=2, color = 'g', label='UCL')
plt.axhline(y=lcl, xmin=0, xmax=1, linewidth=2, color = 'b', label='LCL')
plt.legend()

plt.show()