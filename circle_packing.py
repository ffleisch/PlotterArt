import circles_in_circles as cc
import numpy as np
from matplotlib import pyplot as plt, patches



def largest_possible_radius(x,y,circles):
    dists=[np.sqrt((x-c[0])**2+(y-c[1])**2)-c[2] for c in circles]
    return np.min(np.abs(dists))


n=10000
circles=[]
circles.append((0,0,0.1))

def reps_from_r(r):
    return 1 if r<1 else int(r+3)
def spacing_from_r(r):
    return r/100+0.05

if __name__=="__main__":


    for i in range(n):
        x,y=(np.random.rand(2)-0.5)*2*10
        #r=cc.largest_possible_radius(x,y,circles)
        r=largest_possible_radius(x,y,circles)
        r-=0.02
        reps=reps_from_r(r)
        spacing=spacing_from_r(r)
        if r<0.02:
            continue
        for j in range(reps):
            r_smaller=r-j*spacing
            if r_smaller<0:
                break
            circles.append((x,y,r_smaller))

    for c in circles:
        cc.draw_circle(*c)

    plt.gca().set_aspect("equal")
    plt.xlim(-10,10)
    plt.ylim(-10,10)
    plt.show()