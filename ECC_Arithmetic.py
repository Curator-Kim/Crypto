from Algorithm import expand_gcd
def divide_mod(a,p):
    # p为模数
    # 返回a的逆元
    return expand_gcd(a,p)[1]%p

class ECC(object):
    def __init__(self,a,b,p,G=None,n=None):
        """ y^2=x^3+ax+b mod p, G--基点, n--阶 """
        self.a=a
        self.b=b
        self.p=p
        self.G=G
        self.n=n
    
def ECC_add(ECC,P,Q):
    """  a,b,p为椭圆曲线参数
     Q,P为两个点 """
    R=[0,0]
    if P==[-1,-1]:return Q
    if Q==[-1,-1]:return P
    if P==Q:
        lumda=((3*P[0]*P[0]+ECC.a)%ECC.p)*divide_mod(2*P[1]%ECC.p,ECC.p)%ECC.p
        R[0]=(lumda*lumda-P[0]-Q[0])%ECC.p
        R[1]=(lumda*(P[0]-R[0])-P[1])%ECC.p
    elif P[0]==Q[0]:
        return [-1,-1]
    else:
        lumda=((Q[1]-P[1])%ECC.p)*divide_mod((Q[0]-P[0])%ECC.p,ECC.p)%ECC.p
        R[0]=(lumda*lumda-P[0]-Q[0])%ECC.p
        R[1]=(lumda*(P[0]-R[0])-P[1])%ECC.p
    return R

def ECC_multiply_fast(ECC,P,n):#return P*n
    result=[-1,-1]
    tmp=P
    if P==[-1,-1]:return P
    while(n!=0):
        if n&1==1:
            result=ECC_add(ECC,result,tmp)
        tmp=ECC_add(ECC,tmp,tmp)
        n>>=1
    return result

def ECC_subtract(ECC,P,Q):
    # return P-Q
    if P==Q:return [-1,-1]
    if Q==[-1,-1]:return P
    Q[1]=(-Q[1])%ECC.p
    return ECC_add(ECC,P,Q)

if __name__=="__main__":
    ecc1=ECC(1,6,11)
    print(ECC_multiply_fast(ecc1,[2,7],7))
    print(ECC_multiply_fast(ecc1,[8,8],7))
    print(ECC_subtract(ecc1,[2,7],[3,6]))
    print(ECC_multiply_fast(ecc1,[2,7],3))
    print(ECC_add(ecc1,[10,9],ECC_multiply_fast(ecc1,[7,2],3)))