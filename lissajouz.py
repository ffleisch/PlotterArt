import numpy
from matplotlib import pyplot as plt
import numpy as np
import utilities



def lissajouz(a=2,b=1,phase=0.0,n_steps=100,derivative=False):
    steps=np.linspace(0,np.pi*2,n_steps,endpoint=False)
    points=np.zeros((len(steps),2))

    derivatives=None
    if derivative:
        derivatives=np.zeros((len(steps),2))

    points=np.zeros((len(steps),2))
    gcd=np.gcd(a,b)
    a/=gcd
    b/=gcd

    for i,t in enumerate(steps):
        points[i,0]=np.sin(t*a)
        points[i,1]=np.cos((t+phase)*b)
    if derivative:
        for i,t in enumerate(steps):
            derivatives[i,0]=a*np.cos(t*a)
            derivatives[i,1]=-b*np.sin((t+phase)*b)
    if derivative:
        ret=(points,derivatives)
    else:
        ret=points
    return ret
n=19
if __name__=="__main__":
    lines_a=[]
    lines_b=[]
    for i in range(1,n+1):
        for j in range(1,n+1):
            gcd=np.gcd(i,j)
            figure=lissajouz(i,j,n_steps=100*(int)(i/gcd+j/gcd))
            #figure=lissajouz(i,j,phase=np.pi*(i-1)/float(n-1),n_steps=100+100*(int)(i/gcd+j/gcd))
            figure[:,0]+=i*2.5
            figure[:,1]+=j*2.5

            if gcd>1:
                lines_b.append(figure)
            else:
                lines_a.append(figure)

                plt.plot(figure[:,0],figure[:,1])

    plt.gca().set_aspect("equal")
    plt.show()

    out=utilities.paper()
    utilities.add_line_list(out,lines_a)
    utilities.add_line_list(out,lines_b)
    out.save_svg("svgOut/lissajouz.svg")
