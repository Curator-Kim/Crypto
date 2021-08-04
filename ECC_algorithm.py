import random
from Algorithm import fast_mod
def LucasSequence(p,x,y,k):
    delta=x*x-4*y
    u=1
    v=x
    r=k.bit_length()
    for i in range(r-1,-1):
        u,v=u*v%p,(v*v+delta*u*u)/2%p
        if (k>>i)&1==1:
            u,v=(x*u+v)/2%p,(x*v+delta*u)/2%p
    return u,v


def getSquareRoot(g,p):
    """ 
    二次剩余求解
    0<g<p
    return None -> no SquareRoot 
    """
    if p&0b11==3:
        u=(p-3)>>2
        y=fast_mod(g,u+1,p)
        z=y*y%p
        if z==g:
            return y
        return None
    elif p&0b111==5:
        u=(p-5)>>3
        z=fast_mod(g,2*u+1,p)
        if z%p==1:
            y=fast_mod(g,u+1,p)
            return y
        elif z%p==p-1:
            y=fast_mod(4*g,u,p)*2*g%p
            return y
        return None
    elif p&0b111==1:
        y=g
        u=(p-1)>>3
        while True:
            x=random.randint(0,p-1)
            U=LucasSequence(p,x,y,4*u+1)%p
            V=LucasSequence(p,x,y,4*u+1)%p
            if V*V%p==4*y%p:
                return V/2%p
            if U%p!=1 and U%p!=p-1:
                return None
    return None

def ypb2yp(a,b,point,p):
    alpha=(point[0]*point[0]*point[0]+a*point[0]+b)%p
    beta=getSquareRoot(a,p)
    if beta==None:
        print("no square root!")
        return 
    if beta&1==point[1]:
        point[1]=beta
    else: point[1]=p-beta
    return point