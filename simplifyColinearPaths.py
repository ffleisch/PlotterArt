import matplotlib.colors
import svgpathtools
from matplotlib import pyplot as plt
import numpy as np
import networkx
from skspatial.objects import Line, Points
paths, attributes = svgpathtools.svg2paths("svgIn/0005.svg")

all_endpoints = [p.start for p in paths]
all_endpoints.extend([p.end for p in paths])

points = np.array(all_endpoints)

plt.scatter(np.real(points), np.imag(points))
plt.show()

open_points = {}
'''
for p in paths:
    print(p)
    if p.start in open_points:
        other = open_points[p.start]
        if not other == p:
            if other.end == p.start:
                del open_points[p.start]
                other.extend(p)
                sawp = True
            elif other.start == p.start:
                del open_points[p.start]
                other.reverse()
                other.extend(p)
                swap = True
        open_points[other.start] = other
        open_points[other.end] = other
    elif p.end in open_points:
        other = open_points[p.end]
        if not other == p:
            if other.end == p.end:
                del open_points[p.end]
                other.reverse()
                p.extend(other)
            elif other.start == p.end:
                del open_points[p.end]
                p.extend(other)
        open_points[p.start] = p
        open_points[p.end] = p
    else:
        open_points[p.start] = p
        open_points[p.end] = p
        '''

# paths = list(open_points.values())

graph = networkx.Graph()

for p in paths:
    for e in p:
        graph.add_edge(e.start, e.end, element=e)

print(graph)
new_paths = []
p = svgpathtools.Path()
for s, e in networkx.edge_dfs(graph):
    edge=graph.get_edge_data(s,e)
    #print(edge)
    if edge:
        #plt.plot((np.real(s), np.real(e)), (np.imag(s), np.imag(e)),solid_capstyle="butt")
        edge=edge["element"]
        #if edge_type == "forward" or edge_type == "reverse":
        if len(p)==0:
            p.append(edge)#.reversed())
        else:
            if (p[-1].start==edge.start or p[-1].start==edge.end):
                p[-1]=p[-1].reversed()
            if edge.start==p[-1].end:
                p.append(edge)
            elif edge.end==p[-1].end:
                p.append(edge.reversed())
            else:
                #if edge_type!="nontree":
                #    continue
                new_paths.append(p)
                p = svgpathtools.Path()
                p.append(edge)#.reversed())
if len(p)>0:
    new_paths.append(p)
#plt.gca().invert_yaxis()
#plt.gca().set_aspect("equal")
#plt.show()
#for e in networkx.dfs_edges(graph):
#    print(graph[e[0]][e[1]]["element"])
print(networkx.components.number_connected_components(graph))
print(len(new_paths))
print(len(paths))

paths=new_paths
new_paths=[]

def collinear(p0, p1, p2):
    #x1, y1 = p1[0] - p0[0], p1[1] - p0[1]
    v1=p1-p0
    #x2, y2 = p2[0] - p0[0], p2[1] - p0[1]
    v2=p2-p0
    #return abs(x1 * y2 - x2 * y1) < 1e-12
    print(abs(np.real(v1) * np.imag(v2) - np.real(v2) * np.imag(v1)))
    return abs(np.real(v1) * np.imag(v2) - np.real(v2) * np.imag(v1)) < 1e-1

def line_fit(s,e,points):
    p1=imag_to_tupel(s)
    dir=s-e
    normal=(-np.imag(dir),np.real(dir))
    normal_magnitude=np.abs(dir)
    sum=0
    for p in points:
        d_dir=(p[0]-p1[0],p[1]-p1[1])

        dotp=normal[0]*d_dir[0]+normal[1]*d_dir[1]
        dist=dotp/normal_magnitude
        sum+=dist**2
    return sum/len(points)

def imag_dotp(a,b):
    return np.real(a)*np.real(b)+np.imag(a)*np.imag(b)
def point_is_forward(s,e,p):
    return imag_dotp(e-s,p-e)>=0

def imag_to_tupel(p):
    return (np.real(p),np.imag(p))

for p in paths:
    current_line=None
    merged_points=[]
    new_p=svgpathtools.Path()
    print("another path")
    for e in p:

        if isinstance(e,svgpathtools.Line):
            #print(e)
            if e.start==e.end:
                continue
            #if current_line:
                #print(current_line.end==e.start,current_line.end==e.end)
            #print(merged_points)
            if e.end==1083.627+619.1j:
                print("ohn no")
            if current_line and (current_line.start==e.end and current_line.end==e.start):
                print("oof")

            if current_line and current_line.end==e.start and point_is_forward(current_line.start,current_line.end,e.end) and line_fit(current_line.start,e.end,merged_points)<1e-5:#collinear(current_line.start,current_line.end,e.end):#(e.joins_smoothly_with(current_line)):
                #current_line.end=e.end
                #print("new join",(current_line.start,e.end))
                #print(current_line.end==e.start,current_line.end==e.end)
                current_line=svgpathtools.Line(current_line.start,e.end)
                #print(line_fit(current_line,merged_points))
                merged_points.append(imag_to_tupel(e.end))
            else:
                if current_line:
                    new_p.append(current_line)
                current_line=e
                merged_points=[imag_to_tupel(e.start),imag_to_tupel(e.end)]
        else:
            if current_line:
                new_p.append(current_line)
                current_line=None
                merged_points=[]

            new_p.append(e)

    if current_line:
        new_p.append(current_line)
        current_line=None
        merged_points=[]
    if len(new_p)>0:
        new_paths.append(new_p)

paths=new_paths

cols = list(matplotlib.colors.TABLEAU_COLORS.values())
for i, p in enumerate(paths):
    #c = cols[i % len(cols)]
    for j,l in enumerate(p):
        s = l.start
        e = l.end
        intensity=j/len(p)
        c=cols[0]#(intensity,intensity,intensity)
        plt.plot((np.real(s), np.real(e)), (np.imag(s), np.imag(e)), c=c, alpha=0.3, linewidth=1+15*intensity,zorder=1-intensity,solid_capstyle="round")
points_in_dict = list(open_points.keys())
plt.scatter(np.real(points_in_dict), np.imag(points_in_dict))
plt.gca().invert_yaxis()
plt.gca().set_aspect("equal")
plt.show()
svgpathtools.disvg(paths=paths, filename="svgOut/simplified.svg", openinbrowser=True)
print("saved svg")