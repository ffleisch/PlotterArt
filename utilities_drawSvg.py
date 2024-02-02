import drawsvg
import drawsvg as svg
import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np



def din_size(din=2):
    din_a0=(840.8964152537145430311254762332148950400342623567845108132260859,1189.2071150027210667174999705604759152929720924638174130190022247)
    return (int(din_a0[0]/(np.sqrt(2)**din)),int(din_a0[1]/(np.sqrt(2)**din)))



def paper(din=2):
    shape=din_size(din)
    return svg.Drawing(width=shape[0],height=shape[1], origin="top-left")

def mm(num):
    return "%fmm"%num


def add_line_list(dwg,lines,closed=True):

    path = svg.Path(fill_rule="evenodd", stroke="black",stroke_width=0.5, fill="none")

    commandstr=[]

    for i, c in enumerate(lines):
        commandstr.append("M%g,%g "%(c[0][0],c[0][1]))
        commandstr.extend(["L%g,%g "%(p[0],p[1]) for p in c[1:,:]])
        if closed:
            commandstr.append("Z")
        #print("\r%d%%" % int(100 * i / len(lines)), end="")
    commandstr="".join(commandstr)
    path.append(commandstr)
    dwg.append(path)


def approx_circle_bezier(x,y,r):
    str="m 1 0, a -1 0"

    return str


def add_circle_list(dwg,circles):

    path = svg.Path(fill_rule="evenodd", stroke="black",stroke_width=0.5, fill="none")
    for c in circles:
        dc=drawsvg.Circle(c[0],c[1],c[2],fill="none",stroke="black",stroke_width=0.5)
        dwg.append(dc)
    dwg.append(path)

epsilon=1e-7
def clip_line_to_rect(p1, p2, b, t, l, r):
    #d,u=(d,u) if d<u else (u,d)
    #l,r=(l,r) if l<r else (l,r)
    if (b<=p1[1]<=t and b<=p2[1]<=t and l<=p1[0]<=r and l<=p2[0]<=r):
        return (p1, p2)
        #return (None,None)

    axn=p1[0]#min(p1[0], p2[0])
    ayn=p1[1]#min(p1[1], p2[1])
    bxn=p2[0]#max(p1[0], p2[0])
    byn=p2[1]#max(p1[1], p2[1])
    if(axn<l and bxn<l):
        return (None,None)

    if(axn>r and bxn>r):
        return (None,None)
    if(ayn<b and byn<b):
        return (None,None)
    if(ayn>t and byn>t):
        return (None,None)

    #plt.plot((p1[0],p2[0]),(p1[1],p2[1]),alpha=0.5,c="y")
    i1=line_intersect((axn,ayn), (bxn,byn), (l, b), (l , b+1))
    if i1 is not None:
        #plt.scatter(i1[0],i1[1],c="r")
        if axn<i1[0]:
            axn=i1[0]
            ayn=i1[1]
        if bxn<i1[0]:
            bxn=i1[0]
            byn=i1[1]
    i2=line_intersect((axn,ayn), (bxn,byn), (l, b), (l+1, b ))
    if i2 is not None:
        #plt.scatter(i2[0],i2[1],c="g")
        if ayn<i2[1]:
            axn=i2[0]
            ayn=i2[1]
        if byn<i2[1]:
            bxn=i2[0]
            byn=i2[1]
    i3=line_intersect((axn,ayn), (bxn,byn), (r, t), (r , t+1))
    if i3 is not None:
        #plt.scatter(i3[0],i3[1],c="b")
        if axn>i3[0]:
            axn=i3[0]
            ayn=i3[1]
        if bxn>i3[0]:
            bxn=i3[0]
            byn=i3[1]
    i4=line_intersect((axn,ayn), (bxn,byn), (r, t), (r+1, t ))
    if i4 is not None:
        #plt.scatter(i4[0],i4[1],c="y")
        if ayn>i4[1]:
            axn=i4[0]
            ayn=i4[1]
        if byn>i4[1]:
            bxn=i4[0]
            byn=i4[1]
    #if axn>bxn or ayn>byn:
    #    return (None,None)

    #plt.plot((axn,bxn),(ayn,byn),alpha=0.5,c="r")
    if not( (b-epsilon<=ayn<=t+epsilon and b-epsilon<=byn<=t+epsilon and l-epsilon<=axn<=r+epsilon and l-epsilon<=bxn<=r+epsilon)):

        #plt.plot((axn,bxn),(ayn,byn),alpha=0.5,c="b")
        return (None,None)

    #if axn==bxn and not l<=axn<=r:

    #    return (None,None)

    #if ayn==byn and not b<=ayn<=t:
    #    return (None,None)
    return ((axn,ayn),(bxn,byn))


def line_intersect(a,b,c,d):
    line_1=line_to_homogenous(a,b)
    line_2=line_to_homogenous(c,d)

    intersection=np.cross(line_1,line_2)
    #print(intersection)
    if intersection[2]==0:
        return None
    return intersection[0:2]/intersection[2]

def line_to_homogenous(a,b):
    return np.array((a[1]-b[1],b[0]-a[0],a[1]*(a[0]-b[0])-a[0]*(a[1]-b[1])))


def clip_line_list_to_rect(inp,b,t,l,r):
    out=[]
    for line in inp:
        #print(line[0],line[1])
        p1,p2=clip_line_to_rect(line[0],line[1],b,t,l,r)
        if p1 is not None:
            out.append((p1,p2))
    return np.array(out)

if __name__=="__main__":

    a=(1.3,1.2)
    b=(0,0.1)
    c=(2,1)
    d=(5,2)
    e=line_intersect(a,b,c,d)
    plt.plot((a[0],b[0]),(a[1],b[1]))
    plt.plot((c[0],d[0]),(c[1],d[1]))
    plt.scatter(e[0],e[1])
    plt.show()

    d=0
    l=0
    r=2
    u=0.5


    rect=patches.Rectangle((l,d),r-l,u-d,color="r",fill=False)
    plt.gca().add_patch(rect)

    plt.plot((a[0],b[0]),(a[1],b[1]),alpha=0.2)
    e,f=clip_line_to_rect(a,b,d,u,l,r)

    print(e,f)
    if(e is not None):
        plt.plot((e[0],f[0]),(e[1],f[1]))

    plt.gca().set_aspect("equal")
    plt.show()

    #for i in range(0,10):
    #    print(din_size(i))
    #test=paper()

    #test.save_svg("test.svg")