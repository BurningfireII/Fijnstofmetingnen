# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 16:19:52 2024

@author: daana
"""
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress as linregress
from scipy.optimize import curve_fit as cf
import locale

def interpolate(x,N):
    previous = 0
    for i in range(N):
        DI = len(x[previous:(len(x)-1)])/(N - i)
        New = previous + round(DI)
        if New + 1 < len(x):
            av = (x[New]+x[New+1])/2
        else:
            av = x[New]
        temp = np.append(x[:New],av)
        x = np.append(temp,x[New:])
        previous = New
    return x
        
def Norm_corr(x1, x2):
    
    a = (x1 - np.mean(x1)) / (np.std(x1) * len(x1))
    b = (x2-np.mean(x2)) / (np.std(x2))
    c = np.correlate(a, b, mode='full')
    
    return c

def smooth(x, kern):
    kernel = np.ones(kern) / kern
    smooth = np.convolve(x, kernel, mode='same')
    return smooth

def Z_test(data, ex):
    
    sqn = np.sqrt(np.size(data))
    std = np.std(data)
    mean = np.mean(data)
    
    Z = ((mean - ex)/(std*sqn))
    
    return Z
df = pd.read_csv(r'C:\Users\daana\Documents\Metingen fijnstof\measurementsWOT.txt') #reads data from csv

Data_1 = df.to_numpy()
Data_1 = Data_1.transpose()[3]

df = pd.read_csv(r'C:\Users\daana\Documents\Metingen fijnstof\measurementsWT.txt') #reads data from csv

Data_2 = df.to_numpy()
Data_2 = Data_2.transpose()[3]

df = pd.read_csv(r'C:\Users\daana\Documents\Metingen fijnstof\time.txt') #reads data from csv

times = df.to_numpy()
time = np.array([])
times.transpose()
Data_1 = Data_1[793:]
Data_2 = Data_2[809:]
Data_1 = interpolate(Data_1, 15)
Delta = np.abs(Data_1 - Data_2)

print("gemiddelde fijnstof niveaus")
print(np.mean(Data_1))
print(np.mean(Data_2), "\n")

s_1 = smooth(Data_1,10)
s_2 = smooth(Data_2, 10)
corr = Norm_corr(Data_1, Data_2)
res = abs(s_1-s_2)

print("NCC\n",np.max(corr),"\n")

U = 2*Delta/ (Data_1 + Data_2)
Us = 2* res/ (s_1 + s_2)

z_val = Z_test(U, 0.05)

print("Z-waarde: ", z_val)
print(np.mean(U))
print(3*np.std(U))
#print(U, Us)
for i, t in enumerate(times):
    if t[2] < 10:
        h = "0" + str(t[2])
    if t[3] < 10:
        m = "0" + str(t[3])
    else:
        h = str(t[2])
        m = str(t[3])
    time = np.append(time,('(' + str(t[0]) + '/' + str(t[1]) + ') ' + h +':'+ m))
    
time = time[809:]

ticks = 76

locale.setlocale(locale.LC_NUMERIC, "de_DE")
plt.rcdefaults()
plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams['axes.formatter.use_locale'] = True


plt.rcParams['errorbar.capsize'] = 4
plt.figure()   
plt.plot(corr)
plt.show()
#print(time)
plt.figure()
plt.plot(time,Data_2, c='k', ls='-', label="sensor 1")
plt.plot(time,Data_1, c='r', ls=':', label="sensor 2")
plt.xticks(range(0, len(time), ticks), time[::ticks], rotation=45)
plt.legend()
plt.grid(color='k', ls='--', alpha=0.25)
plt.xlabel(r'$t[(M/d)h:m]$')
plt.ylabel(r'$PM_{10}[\mu g \ m^{-3}]$')
plt.xlim(0, 731)
plt.savefig("Resultatenfs.pdf",bbox_inches='tight')
plt.show()

plt.figure()
plt.plot(Data_1-Data_2)
plt.xticks(range(0, len(time), ticks), time[::ticks], rotation=45)
plt.show()

plt.figure()
plt.plot(s_1)
plt.plot(s_2)
plt.xticks(range(0, len(time), ticks), time[::ticks], rotation=45)
plt.show()

plt.figure()
plt.plot(np.abs(s_1-s_2))
plt.xticks(range(0, len(time), ticks), time[::ticks], rotation=45)
plt.show()