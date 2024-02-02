import numpy as np
from matplotlib import pyplot as plt, patches
import opensimplex as ops

import utilities_drawSvg


def draw_circle(x,y,r):
    c=patches.Circle((x,y),r,fill=None)
    #print(x,y,r)
    plt.gca().add_patch(c)

def noise_loop(r,t):
    return ops.noise2(np.sin(t*2*np.pi)*r,np.cos(t*2*np.pi)*r)

def largest_possible_radius(x,y,circles):
    dists=[np.sqrt((x-c[0])**2+(y-c[1])**2)-c[2] for c in circles]
    return np.min(dists)

if __name__=="__main__":

    n=600

    major_radius=7
    minor_radius=1

    dec=0.7
    radius_decrease=lambda x:x*dec-0.1
    gap_decrease=lambda x:x*dec


    gap=.05

    #noise_scale=1.5
    #noise_amplitude=1.5

    noise_scale=3
    noise_amplitude=1

    ops.random_seed()

    #radii=[1+noise_amplitude*noise_loop(noise_scale,i/n)for i in range(n)]
    radii=[noise_amplitude*(1+0.5*np.sin(noise_scale*2*np.pi*i/n))for i in range(n)]

    #plt.plot(radii)
    #plt.show()


    circles_outer=[]
    for i,r in enumerate(radii):
        c=(major_radius* np.sin((i / len(radii)) * 2 * np.pi),major_radius*np.cos((i / len(radii)) * 2 * np.pi), r*minor_radius)
        circles_outer.append(c)



    new_major_radius=major_radius
    new_number=n
    new_gap=gap
    draw_circles=[(x,y,r-gap) for x,y,r in circles_outer if r>gap]

    for m in range(20):
        new_major_radius=radius_decrease(new_major_radius)
        new_gap=gap_decrease(new_gap)
        new_number=int((new_major_radius/major_radius)*n)
        new_circles=[]
        for i in range(new_number):
            x=new_major_radius* np.sin((i / new_number) * 2 * np.pi)
            y=new_major_radius*np.cos((i / new_number) * 2 * np.pi)
            new_r=largest_possible_radius(x,y,circles_outer)
            if new_r>0:
                c=(x,y, new_r)
                new_circles.append(c)
                if new_r>gap:
                    d_c=(x,y,new_r-gap)
                    draw_circles.append(d_c)
        circles_outer.extend(new_circles)
        #for c in new_circles:
        #    draw_circle(*c)


    for c in draw_circles:
        draw_circle(*c)
    plt.gca().set_aspect("equal")
    plt.xlim(-10,10)
    plt.ylim(-10,10)

    plt.show()

    out=utilities.paper()
    utilities.add_circle_list(out,draw_circles)
    out.save_svg("svgOut/circles.svg")
