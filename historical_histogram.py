import numpy as np
import matplotlib.pyplot as plt
no_of_bins = 5
data = np.genfromtxt('data.csv',delimiter=',',dtype=str)
values = data[1:,1:5]
for i in range(values.shape[0]):
    for j in range(values.shape[1]):
        values[i,j] = values[i,j].replace('    ','')
        values[i,j] = values[i,j].replace('"','')
values = values.astype(float)
change = values[:,-1]-values[:,0]
swing = values[:,1]-values[:,2]
plt.figure(1)
plt.subplot(211)
plt.hist(change,100,density=True,facecolor='g',alpha=0.75)
plt.xlabel('Change')
plt.ylabel('Probability')
plt.title('Change Probability')
##plt.axis([-450,450,0,0.0025])
plt.grid(True)

plt.subplot(212)
plt.hist(swing,100,density=True,facecolor='g',alpha=0.75)
plt.xlabel('Swing')
plt.ylabel('Probability')
plt.title('Swing Probability')
##plt.axis([100,800,0,0.004])
plt.grid(True)
plt.show()