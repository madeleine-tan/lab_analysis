import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
plt.style.use('default')
rcParams['figure.dpi'] = 150

#import data, set arrays
#NOAA temperature data from Jan 1900 onwards
df = pd.read_csv('./US_average_Temperature.csv')
TBL=df.to_numpy(dtype=float,copy=True)
time=TBL[:,0] # time in months since Jan 15 1900
temp=TBL[:,1] # average monthly temperature

#begin linear least squares
#T = T0 + cos(omega*t) --> T = T0 + beta1*cos(omega*t) + beta2*sin(omega*t) + beta3*t
Ycos  = np.cos((np.pi/6)*time)
Ysin  = np.sin((np.pi/6)*time)

ycos = np.vstack((np.repeat(1,len(Ycos)),Ycos))
x02 = np.concatenate([ycos,Ysin.reshape(1,1453),time.reshape(1,1453)])
xTx2 = np.matmul(x02,x02.T)
xTy2 = np.matmul(x02,temp)
xTt2 = np.matmul(x02,time)

xTx2_inv = np.linalg.inv(xTx2)
betas2 = np.matmul(xTx2_inv, xTy2, xTt2)
T02 = betas2[0]
beta11 = betas2[1]
beta22 = betas2[2]
beta33 = betas2[3]
print(T02)
print(beta11)
print(beta22)
print(beta33)

#Plot data with linear least squares
fig=plt.figure()
ax = fig.add_subplot(111)

plt.scatter(time,temp,color='black')
ax.set_xlim(1333,1453)
ax.set_ylim(25,80)
plt.plot(T02 + (beta11*Ycos) + (beta22*Ysin) + (beta33*time),c='b',ls='--',label="T = 51.34 - 20.26cos(\u03C9t) - 6.89sin(\u03C9t) + 0.0013t")
plt.title("Last 10 years of NOAA temperature data with linear least squares fit")
ax.set_xlabel('months since Jan 1900')
ax.set_ylabel('temperature (F)')
ax.grid(alpha=0.4)
plt.legend(prop={'size': 8})
plt.show()
