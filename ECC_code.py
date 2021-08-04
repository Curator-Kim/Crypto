import math
import ECC_algorithm
def n2bytes(x,k=None):
    if k==None:
        return x.to_bytes(math.ceil(x.bit_length()/8),'big')
    else:
        return x.to_bytes(k,'big')
    
def bytes2n(bytes):
    """ 字节串转换为整数 """
    x=0
    for i in range(len(bytes)):
        x<<=8
        x+=bytes[i]
    return x

def element2bytes(a,k=None):#Zp
    """ 域内元素转字节串 """
    return n2bytes(a,k)

def bytes2element(bytes,p):#Zp
    """ 字节串转域内元素 """
    a=bytes2n(bytes)
    if a>=p:
        print("incorrect bytes!")
        return 0
    return a

def element2n(a):#Zp
    return a

def point2bytes(point,form,k=None):
    """ form=0:压缩表示形式 form=1:未压缩表示 form=2混合表示
    point 为椭圆曲线上的点，为列表形式 """
    X1=n2bytes(point[0],k)
    if form==0:
        ypb=point[1]&1#令ypb为yp~
        if ypb==0:PC=2
        else:PC=3
        S=PC.to_bytes(1,'big')+X1
    elif form==1:
        Y1=element2bytes(point[1],k)
        PC=4
        S=PC.to_bytes(1,'big')+X1+Y1
    elif form==3:
        Y1=element2bytes(point[1],k)
        ypb=point[1]&1
        if ypb==0:PC=6
        else:PC=7
        S=PC.to_bytes(1,'big')+X1+Y1
    return S

def bytes2point(a,b,S,form,p):
    """ form=0:压缩表示形式 form=1:未压缩表示 form=2混合表示 """
    if form==0:
        PC=S[0]
        X1=S[1:]
        xp=bytes2element(X1,p)
        if PC!=2 and PC!=3:
            print("incorrect PC!")
            return None
        if PC==2:ypb=0
        if PC==3:ypb=1
        point=[xp,ypb]
        point=ECC_algorithm.ypb2yp(a,b,point,p)
    elif form==1:
        PC=S[0]
        X1=S[1:(len(S)-1)//2+1]
        Y1=S[(len(S)-1)//2+1:]
        X1=bytes2element(X1,p)
        Y1=bytes2element(Y1,p)
        # print(hex(X1),hex(Y1))
        if PC!=4: 
            print("incorrect PC!")
            return None
        point=[X1,Y1]
    elif form==2:
        PC=S[0]
        X1=S[1:(len(S)-1)//2+1]
        Y1=S[(len(S)-1)//2+1:]
        X1=bytes2element(X1,p)
        if PC!=6 and PC!=7:
            print("incorrect PC!")
            return None
        yp=bytes2element(Y1,p)
        if PC==6: ypb=0
        else: ypb=1
        point=ECC_algorithm.ypb2yp(a,b,[X1,ypb],p)
    if (point[1]*point[1])%p!=((point[0]*point[0]*point[0])%p+(a*point[0])%p+b)%p:
        print(hex(point[0]),hex(point[1]))
        print('a=%x'%a)
        print('b=%x'%b)
        print('p=%x'%p)
        print("error!")
        return None
    return point

def encode(a,b,p,str):
    """ 将字符串编码到椭圆曲线的点上 """
    str=bytes(str,'utf-8')
    n=bytes2n(str)
    if (n<<8)>p: return None
    n<<=8
    point=[n,None]
    for i in range(256):
        point[1]=ECC_algorithm.getSquareRoot(point[0],p)
        if point[1]!=None: break
        point[0]+=1
    return point
    
def decode(point):
    """ 将椭圆曲线上的点还原为字符串 """
    n=point[0]>>8
    str=n2bytes(n)
    return str.decode()

def get_y(a,b,p,n):
    """ 由横坐标得到椭圆曲线上的纵坐标 """
    n=(n*n*n+a*n+b)%p
    y=ECC_algorithm.getSquareRoot(n,p)
    return y