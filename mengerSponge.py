import numpy as np
from matplotlib import pyplot as plt



sizer_array=np.array([[[1,1,1],
              [1,0,1],
              [1,1,1]],

              [[1,0,1],
              [0,0,0],
              [1,0,1]],

              [[1,1,1],
              [1,0,1],
              [1,1,1]]])

state=np.ones((1,1,1))



def iterate(state):
    extent=state.shape
    new_state=np.zeros(np.array(state.shape)*3)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if sizer_array[i,j,k]:
                    new_state[i*extent[0]:(i+1)*extent[0],j*extent[1]:(j+1)*extent[1],k*extent[2]:(k+1)*extent[2]]=state
    return new_state

for i in range(2):
    state=iterate(state)

positions=np.argwhere(state)
np.savetxt("menger.csv",positions,fmt="%d",delimiter=",")
print(positions)
print(len(positions))

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(positions[:,0],positions[:,1],positions[:,2])
plt.show()
