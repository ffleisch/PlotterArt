import matplotlib.pyplot as plt
import numpy as np
import sympy
import svgpathtools as spt

square_positions={1:np.array((0.25,0.75)),3:np.array((0.75,0.75)),7:np.array((0.25,0.25)),9:np.array((0.75,0.25))}

def circle(p,r):
    p=complex(p[0],p[1])
    paths=[spt.Arc(p+r,complex(r,r),0,False,True,p-r),spt.Arc(p-r,complex(r,r),0,False,True,p+r)]
    return paths



def make_square(n,base_coords):
    r=0.05
    positions=[]
    for o,coords in square_positions.items():
        if sympy.isprime(n+o):
            print(n+o)
            positions.append(base_coords+coords)
    #if len(positions)==0:
    line_path=spt.Path()
    circles_path=spt.Path()
    if n==0:
        positions.append(base_coords+(0.5,0.75))
        positions.append(base_coords+(0.5,0.5))
        line_path.append(spt.Line(complex(*positions[0]),complex(*positions[1])))
        line_path.append(spt.Line(complex(*positions[0]),complex(*positions[2])))
        line_path.append(spt.Line(complex(*positions[2]),complex(*positions[3])))
        #circles_path.extend(circle((base_coords[0]+0.5,base_coords[1]+0.25),r))
        #circles_path.extend(circle((base_coords[0]+0.5,base_coords[1]+0.5),r))
    else:
        if len(positions)==1:
            circles_path.extend(circle(positions[0],r))
            #plt.plot(positions[0][0],positions[0][1])
        if len(positions)==2:
            line_path.append(spt.Line(complex(*positions[0]),complex(*positions[1])))
            #plt.plot(positions[:][0],positions[:][1])
        if len(positions)==3:
            line_path.append(spt.Line(complex(*positions[0]),complex(*positions[1])))
            line_path.append(spt.Line(complex(*positions[1]),complex(*positions[2])))
            line_path.append(spt.Line(complex(*positions[2]),complex(*positions[0])))
        if len(positions)==4:
            line_path.append(spt.Line(complex(*positions[0]),complex(*positions[1])))
            line_path.append(spt.Line(complex(*positions[1]),complex(*positions[3])))
            line_path.append(spt.Line(complex(*positions[3]),complex(*positions[2])))
            line_path.append(spt.Line(complex(*positions[2]),complex(*positions[0])))
    line_path.extend(circles_path)
    return line_path

def make_grid(nx,ny,offset):
    path=spt.Path()
    o=complex(offset[0],offset[1])
    for i in range(1,nx):
        path.append(spt.Line(complex(i,0)+o,complex(i,ny)+o))

    for i in range(1,nx):
        path.append(spt.Line(complex(0,i)+o,complex(nx,i)+o))
    return path

if __name__=="__main__":

    all_paths=[]
    block_offsets=np.array([(1,3),
                   (0,2),
                   (1,2),
                   (2,2),
                   (0,1),
                   (1,1),
                   (2,1),
                   (0,0),
                   (1,0),
                   (2,0)])

    for k in range(10):
        offset=block_offsets[k,:]*11-0.5

        for i in range(10):
            for j in range(10):
                lp=make_square(1000*k+100*i+10*j,offset+np.array((i,j)))
                if len(lp)>0:
                    all_paths.append(lp)
        all_paths.append(make_grid(10,10,offset))
    print("yeet")
    plt.show()
    dwg=spt.disvg(paths=all_paths, filename="svgOut/prime_table.svg", openinbrowser=True,paths2Drawing=True)
    print(dwg)
    
    print("saved svg")
