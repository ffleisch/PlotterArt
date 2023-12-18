import numpy as np
from scipy.spatial import Voronoi,voronoi_plot_2d

from matplotlib import pyplot as plt, patches

import utilities
rot_mat=lambda angle:np.array([[np.cos(-angle),-np.sin(-angle)],
                  [np.sin(-angle),np.cos(-angle)]])
num=8
num_2=3
r=1
reps=6
points=np.array([(np.sin(2*np.pi*i/num),np.cos(2*np.pi*i/num)) for i in range(num)])
points=np.array([np.matmul(points,rot_mat(-2*np.pi*i/num_2))+r*np.array((np.sin(2*np.pi*i/num_2),np.cos(2*np.pi*i/num_2))) for i in range(num_2)])
points=np.concatenate(points)

#points=np.array([(np.random.randn(),np.random.randn())for i in range(num)])

plt.scatter(points[:,0],points[:,1])
plt.gca().set_aspect("equal")
plt.show()

def region_area(vor,r):
    loop=vor.vertices[r]
    f=loop[:,0]*np.roll(loop[:,1],1)-np.roll(loop[:,0],1)*loop[:,1]
    a=0.5*np.sum(f)
    return a

def edges_from_voronoi(vor):
    indices=[]
    for e in vor.ridge_vertices:
        #print(e)
        if e[0]!=-1 and e[1]!=-1:
            if e[0]<e[1]:
                indices.append(e)

    lines=[(vor.vertices[e[0]],vor.vertices[e[1]]) for e in indices]
    return lines
for i in range(reps):
    vor=Voronoi(points)
    #lines=edges_from_voronoi(vor)
    #for l in lines:
    #   plt.plot((l[0][1],l[1][1]),(l[0][0],l[1][0]),c="k",alpha=0.5)

    voronoi_plot_2d(vor)



    plt.gca().set_aspect("equal")
    plt.show()



    #if i < 3:
    points=np.concatenate([vor.points,vor.vertices])
    #else:
    #   points=vor.vertices
lines=edges_from_voronoi(vor)

def format_lines(lines,w=1):
    paper_size=np.array(utilities.din_size(2))
    margin=10
    center_offset=paper_size/2
    print(center_offset)
    lines*=(center_offset[0]/w)
    lines+=center_offset

    for l in lines:
        plt.plot((l[0][1],l[1][1]),(l[0][0],l[1][0]),c="k",alpha=0.5)
    plt.gca().set_aspect("equal")
    plt.show()


    l=margin
    r=paper_size[0]-margin
    d=margin
    u=paper_size[1]-margin

    lines=utilities.clip_line_list_to_rect(lines,d,u,l,r)

    rect=patches.Rectangle((l,d),r-l,u-d,color="r",fill=False)

    plt.gca().add_patch(rect)
    for l in lines:
        plt.plot((l[0][0],l[1][0]),(l[0][1],l[1][1]),c="k",alpha=0.5)
    plt.gca().set_aspect("equal")
    plt.show()


    return lines

lines=np.array(lines)
lines=format_lines(lines)
out=utilities.paper()
utilities.add_line_list(out,lines,closed=False)
out.save_svg("svgOut/vor.svg")