import math

import numpy as np
from matplotlib import pyplot as plt
import lissajouz
import utilities


a=4
b=3

reps=a*b*38
resolution=200
major,derivative=lissajouz.lissajouz(a,b,n_steps=reps*resolution,derivative=True)
#major=np.array([(i/(200*reps),0) for i in range(200*reps)])
#derivative=np.array([(1,0) for i in range(200*reps)])

minor=lissajouz.lissajouz(2,1,n_steps=resolution)

minor[:,0]*=0.5
scale=0.1
transform=np.array([[scale,0],
                    [0,scale]])

points=[]

for i,(p,d) in enumerate(zip(major,derivative)):
    #print(p)
    angle=math.atan2(d[0],d[1])+np.pi/2
    rot_mat=np.array([[np.cos(-angle),-np.sin(-angle)],
                      [np.sin(-angle),np.cos(-angle)]])
    mat=rot_mat@transform




    minor_offset=minor[i%resolution,:]
    point=mat@minor_offset+p

    points.append(point)
    #fwd=rot_mat@(.1,0)
    #print(angle,fwd)
    #plt.plot((p[1],p[1]+fwd[1]),(p[0],p[0]+fwd[0]))



    #plt.plot((p[1],p[1]+d[1]*.1),(p[0],p[0]+d[0]*.1))
points.append(points[0])
points=np.array(points)


plt.plot(points[:,0],points[:,1],linewidth=0.5)
plt.gca().set_aspect("equal")
plt.show()

out=utilities.paper()
utilities.add_line_list(out,[points*200])
out.save_svg("svgOut/spirographish.svg")

