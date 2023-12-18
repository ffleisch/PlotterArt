from matplotlib import pyplot as plt
import numpy as np

from scipy.spatial import Voronoi,voronoi_plot_2d



n_points=19

points=np.random.random((n_points,2))

w=1
points[:,0]*=w
w=2

def make_virtual_points(points,w,h):
    n_points=points.shape[0]
    v_points=np.zeros((n_points*5,2))
    v_points[0:n_points,:]=points
    v_points[n_points:n_points*2]=points*[-1,1]
    v_points[n_points*2:n_points*3]=points*[1,-1]
    v_points[n_points*3:n_points*4]=points*[-1,1]+[2*w,0]
    v_points[n_points*4:n_points*5]=points*[1,-1]+[0,2*h]
    return v_points


def calc_centroids(vor,n_points):
    centroids=np.zeros((n_points,2))
    s=0
    for i in range(n_points):
        p=vor.point_region[i]
        #print(p)
        region=vor.regions[p]
        loop=vor.vertices[region]
        #area=0.5*np.abs(np.dot(loop[:,1]+np.roll(loop[:,1],1),loop[:,0]-np.roll(loop[:,0],1)))
        #s+=area
        #print(area)

        f=loop[:,0]*np.roll(loop[:,1],1)-np.roll(loop[:,0],1)*loop[:,1]
        a=0.5*np.sum(f)
        #print(a)
        centroids[i,0]=np.sum((loop[:,0]+np.roll(loop[:,0],1))*f)/(6*a)
        centroids[i,1]=np.sum((loop[:,1]+np.roll(loop[:,1],1))*f)/(6*a)
        plt.plot((vor.points[i][0],centroids[i,0]),(vor.points[i][1],centroids[i,1]))
        s+=a
    #print(s)
    return centroids


plt.scatter(points[:,0],points[:,1])
plt.gca().set_aspect("equal")
plt.show()

plt.ion()

point_succession=[]

for i in range(100):
    plt.cla()
    point_succession.append(np.array(points))
    points=make_virtual_points(points,w,1)
    voronoi=Voronoi(points)
    centroids=calc_centroids(voronoi,n_points)
    points=centroids
    #plt.scatter(centroids[:,0],centroids[:,1])
    voronoi_plot_2d(voronoi,ax=plt.gca())

    plt.gca().set_aspect("equal")
    #plt.show()
    plt.pause(0.1)
    plt.draw()

plt.ioff()
plt.show()

point_succession=np.array(point_succession)

for i in range(point_succession.shape[1]):
    plt.plot(point_succession[:,i,0],point_succession[:,i,1])
plt.show()