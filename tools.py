import math
from libnum import s2n
def FFmultiply(a,b,p):#有限域上的乘法运算
    result=0
    i=0
    while(b!=0):
        if(b&0x1==1):result^=(a<<i)
        i+=1
        b>>=1
    return FFmod(result,p)
    
def FFmod(a,b=0x11b):#有限域上的模运算，默认模0x11b
    if(a!=0):
        while(int(math.log(a,2))+1>=int(math.log(b,2))+1):
            tmp=b
            while(int(math.log(a,2))+1>int(math.log(tmp,2))+1): tmp<<=1
            a=a^tmp
    return a
def rotate_left(x,digit):#32比特下的循环左移函数
    return ((x<<digit)&0xffffffff)|(x>>(32-digit))

def mod_add(a,b):#模2的31次方-1的加法的快速实现
    c=a+b
    c=(c&0x7FFFFFFF)+(c>>31)
    return c

def mod_2exp_mul(a,exp):#模2的31次方-1的乘法的快速实现，仅用于a与2的整数次幂相加
    return ((a<<exp)&0x7fffffff)|(a>>(31-exp))

def typeChange(message):
    """ 类型转变，对进来的消息统一转变为数字 """
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

def connect(a,b):
    """ bytes connection """
    b_length=math.ceil(b.bit_length()/8)
    return (a<<(b_length*8))|b

def n2bytes(x,k=None):
    if k==None:
        return x.to_bytes(math.ceil(x.bit_length()/8),'big')
    else:
        return x.to_bytes(k,'big')