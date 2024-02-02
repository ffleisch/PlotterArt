import numpy as np
from matplotlib import pyplot as plt
import twistedPolygons as tp
import svgpathtools as spt
def create_hex_coordinates(rows,width):
    positions=[]
    h=np.sin(np.pi/3)
    for i in range(rows):
        offset=0 if i%2==0 else 0.5
        for j in range(width-i%2):
            positions.append((i*h,j+offset))
    for p in positions:
        plt.scatter(p[0],p[1])
    return np.asarray(positions)

plt.gca().set_aspect("equal")
positions=create_hex_coordinates(26,16)

all_paths=[]
for p in positions:
    #tp.draw_regular_polygon(p,p+(0.5,0),6)
    angle_deg=3
    reps=0
    angle=angle_deg*2*np.pi/360+2*np.pi/3
    all_paths.extend(tp.twist_single(p,p+(0.9*2/3*np.sin(np.pi/3),0),6,angle,reps))
plt.show()

spt.disvg(paths=all_paths, filename="svgOut/twisted_hexagons.svg", openinbrowser=True)
print("saved svg")