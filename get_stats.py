#parse text file and calculate successes
import matplotlib.pyplot as plt
import numpy as np

fi='test'
#read in each line in txt file
with open(fi+'.txt') as f:
    content = f.readlines()

#init empty array
arr=[]

#loop to check if success:
for c in content:
	if (c=='Environment.act(): Primary agent has reached destination!\n') :
		arr.append(1)
	elif c=='Environment.step(): Primary agent ran out of time! Trial aborted.\n':
		arr.append(0)

success=sum(arr)

#create num arr for obs number:
number=range(len(arr))

#clear figure
plt.clf()

#ploat scatter plot
plt.scatter(number,arr,color='green')

#make titles
plt.title("Destination reached vs Ran out of time")
plt.xlabel("trial #")
plt.ylabel("outcome: 1 is Dest. Reached 0 is Ran out of time")
axes = plt.gca()
axes.set_xlim([0,100])
axes.set_ylim([-0.2,1.2])
plt.savefig(fi+'.png')

print 'There were ' + str(success) +' successes out of 100 trials'
