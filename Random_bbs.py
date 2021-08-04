import random
import Algorithm
import time
import math
def generate_big_prime(n):#用于产生大素数
    p=random.randint(2,1<<n)
    p += 2 if p & 1 else 1
    while(Algorithm.MilerRabinTest(p)==1):
        p=(p+2)%(1<<n)
    return p

def generate_big_prime_bbs(n):#用于产生大素数
    p=generate_random_number(n)
    p += 2 if p & 1 else 1
    while(Algorithm.MilerRabinTest(p)==1):
        p=(p+2)%(1<<n)
    return p

def getPQ(digit):#用于获得符合条件的大素数P、Q，digit为n=p*q的比特位数
    p=generate_big_prime(digit//2)
    q=generate_big_prime(math.ceil(digit/2))
    while(p%4!=3):p=generate_big_prime(digit//2)
    while(q%4!=3):q=generate_big_prime(math.ceil(digit/2))
    return p,q

def generate_random_number(digit=128,s=None):
    #digit--所要产生的随机数的位数  s--产生随机数的种子，当不指定s时默认以系统时间为s
    #产生随机数的主函数，每次生成随机数时p、q固定，
    # p,q=getPQ(digit)
    # print(hex(p),hex(q))
    p=0x94c76aed0302ecc3e08c2d614a15dae60d6976feed52d6bcf07fd2076f1eb32f2fa6986b24d59f1eb9cda53cece00292b3d8305a25d6cedf6990c810412d0927
    q=0xb083afdb368a6b9331e245e8babab99561406dd7a620ed3b3b6c6a12271f99887b527638f407047cffb41e922ba4b62dc6d46d34959adb3227ea2308d90532a7
    n=p*q
    if s==None:s=int(time.time())%(1<<digit)
    # print(n,s)
    while Algorithm.expand_gcd(s,n)[0]!=1 or s==0 or s==1:#若s不合法则令s自增至合法
        s=(s+1)%(1<<digit)
    random_number=0
    for i in range(digit):
        s=(s*s)%n
        random_number<<=1
        random_number|=(s&0b1)
    return random_number

if __name__=='__main__':
    # print(getPQ(1024))
    # print(getPQ(256))
    print(generate_random_number(128))
    # print(hex(generate_random_number(64,0xa123)))
    # print(hex(generate_random_number(64,0x74ae863077d2f9a)))
    # print(hex(generate_random_number(64,0x74ae863077d2f9a)))
    # print(hex(generate_random_number(128)))
    # print(hex(generate_random_number(256)))
    # print(hex(generate_random_number(512)))
    # print(hex(generate_random_number(1024)))
    # for i in range(10):
    #     print(hex(generate_random_number(1024)))