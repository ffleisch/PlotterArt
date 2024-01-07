from _ast import pattern

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import svgpathtools as spt



def twist_polygon(center,v1,n,angle):
    alpha=2*np.pi/n
    l=np.cos(alpha/2)/np.cos(np.mod(angle,alpha)-alpha/2)
    d=(v1-center)*l
    mat=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
    return center+d@mat


def draw_regular_polygon(center,v1,n,skip=0):
    positions=np.zeros((n+1,2))
    dir=v1-center
    for i in range(n):
        angle=(i*(1+skip))*2*np.pi/n
        mat=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
        positions[i,:]=center+dir@mat
    positions[n,:]=positions[0,:]
    plt.plot(positions[:,0],positions[:,1])
    path=spt.Path()
    path.extend([spt.Line(complex(*a),complex(*b)) for a,b in zip(positions[0:n,:],positions[1:n+1,:])])
    return path





def test():

    all_paths=[]
    center=np.array([0,0])


    p1=np.array([0,-1])


    n=7
    angle_deg=360/(n*7)+360/n #0.1*360/n

    reps=90
    angle=angle_deg*2*np.pi/360


    #p2=twist_polygon(center,p1,3,angle)

    #plt.scatter(p1[0],p1[1])
    #draw_regular_polygon(center,p1,3)
    #draw_regular_polygon(center,p2,3)
    #plt.scatter(p2[0],p2[1])

    skip=0

    all_paths=[draw_regular_polygon(center,p1,n,skip=skip)]
    for i in range(reps):

        p1=twist_polygon(center,p1,n,angle)
        #p1-=(p1-center)*0.01/np.linalg.norm(p1-center)
        all_paths.append(draw_regular_polygon(center,p1,n,skip=skip))


    plt.gca().set_aspect("equal")
    plt.show()


    cols = list(matplotlib.colors.TABLEAU_COLORS.values())
    for i, p in enumerate(all_paths):
        #c = cols[i % len(cols)]
        for j,l in enumerate(p):
            s = l.start
            e = l.end
            print((np.real(s), np.real(e)), (np.imag(s), np.imag(e)))
            intensity=j/len(p)
            c=cols[0]#(intensity,intensity,intensity)
            plt.plot((np.real(s), np.real(e)), (np.imag(s), np.imag(e)), c=c)#,alpha=0.3, linewidth=1+15*intensity,zorder=1-intensity,solid_capstyle="round")
    return all_paths

def square_array():
    nx=7
    ny=10
    reps=60
    n=3
    all_paths=[]
    for i in range(nx):
        for j in range(ny):
            center=np.array((i+0.5,j+0.5))
            p=np.array((i,j))
            angle=(3)*2*np.pi/360*(-1 if i%2 else 1)*(-1 if j%2 else 1)+2*np.pi/n
            all_paths.append(draw_regular_polygon(center,p,n))
            for k in range(reps):
                p=twist_polygon(center,p,n,angle)
                all_paths.append(draw_regular_polygon(center,p,n))
    return all_paths
if __name__=="__main__":
    #all_paths=square_array()
    all_paths=test()
    plt.gca().set_aspect("equal")
    plt.show()
    spt.disvg(paths=all_paths, filename="svgOut/twisted_polygons.svg", openinbrowser=True)
    print("saved svg")
