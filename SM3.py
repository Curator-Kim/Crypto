import math
from libnum import s2n
def SM3(mes):
    mes,length=typeChange(mes)
    mes,length=padding(mes,length)
    # print(hex(mes))
    hash=Iteration(mes,length)
    return hash

def Iteration(mes,length):
    B=divideGroups(mes,length)
    n=length//512
    V=[0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e]
    for i in range(n):
        V.append(CF(V[i],B[i]))
    return V[n]

def MesExtension(B):
    """ message extension """
    W=[]
    W_1=[]
    for i in range(16):
        W.append(B&0xffffffff)
        B>>=32
    W=W[::-1]
    for i in range(16,68):
        W.append(P(W[i-16]^W[i-9]^rotate_left(W[i-3],15),1)^rotate_left(W[i-13],7)^W[i-6])
    for i in range(0,64):
        W_1.append(W[i]^W[i+4])
    # for i in range(64):
    #     print(hex(W_1[i]))
    return W,W_1

def CF(V,Bi):
    """ Compress Function"""
    H=V&0XFFFFFFFF
    G=(V>>32)&0XFFFFFFFF
    F=(V>>64)&0XFFFFFFFF
    E=(V>>96)&0XFFFFFFFF
    D=(V>>128)&0XFFFFFFFF
    C=(V>>160)&0XFFFFFFFF
    B=(V>>192)&0XFFFFFFFF
    A=(V>>224)&0XFFFFFFFF
    W,W_1=MesExtension(Bi)
    for j in range(0,64):
        # print(j,hex(A))
        SS1=rotate_left((rotate_left(A,12)+E+(rotate_left(T(j),j%32)))%(1<<32),7)
        SS2=SS1^rotate_left(A,12)
        TT1=(FF(A,B,C,j)+D+SS2+W_1[j])%(1<<32)
        TT2=(GG(E,F,G,j)+H+SS1+W[j])%(1<<32)
        D=C
        C=rotate_left(B,9)
        B=A
        A=TT1
        H=G
        G=rotate_left(F,19)
        F=E
        E=P(TT2,0)
    V=((A<<224)|(B<<192)|(C<<160)|(D<<128)|(E<<96)|(F<<64)|(G<<32)|H)^V
    return V

def divideGroups(mes,length):
    B=[]
    for i in range(length//512):
        B.append(mes&((1<<512)-1))
        mes>>=512
    return B[::-1]

def FF(x,y,z,j):
    if 0<=j<=15:
        return x^y^z
    elif 16<=j<=63:
        return (x&y)|(x&z)|(y&z)

def GG(x,y,z,j):
    if 0<=j<=15:
        return x^y^z
    elif 16<=j<=63:
        return (x&y)|(not_32(x)&z)

def T(j):
    if 0<=j<=15:
        return 0x79cc4519
    elif 16<=j<=63:
        return 0x7a879d8a
    else:
        return None

def padding(message,length):
    """ 填充消息，length为消息的长度 """
    paddingLen=(448-length%512)%512
    message=(message<<1)+1
    paddingLen=(paddingLen-1)%512
    if paddingLen>1:
        message<<=paddingLen
    return (message<<64)|length,length+paddingLen+65

def typeChange(message):
    """ 类型转变，对进来的消息统一转变为int """
    if type(message) is bytes:
        length=len(message)*8
        message=bytes2n(message)
    elif type(message) is str :
        length=len(bytes(message,'utf-8'))*8
        message=s2n(message)
    else:length=math.ceil(message.bit_length()/4)*4
    return message,length

def bytes2n(bytes):
    x=0
    for i in range(len(bytes)):
        x<<=8
        x+=bytes[i]
    return x

def not_32(a):
    return a^0xffffffff

def P(X,t):
    if t==0:
        return X^rotate_left(X,9)^rotate_left(X,17)
    elif t==1:
        return X^rotate_left(X,15)^rotate_left(X,23)
    else:
        return None

def rotate_left(x,digit):
    """ 32比特下的循环左移函数 """
    return ((x<<digit)&0xffffffff)|(x>>(32-digit))

if __name__=='__main__':
    print(hex(SM3('abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd')))#0xdebe9ff92275b8a138604889c18e5a4d6fdb70e5387e5765293dcba39c0c5732