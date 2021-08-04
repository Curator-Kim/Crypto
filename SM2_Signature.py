import math
from libnum import s2n
import ECC_Arithmetic
import Algorithm
import ECC_code
import SM3
import random
def Sign(ECC,M,PA,dA,ZA):
    """ 
        a,b,p,G,n皆为椭圆曲线参数
        返回字节串(r,s)
    """
    e=connect(ZA,M)
    e=SM3.SM3(e)
    print(hex(e))
    while(True):
        k=random.randint(1,ECC.n-1)
        # k=0x6CB28D99385C175C94F94E934817663FC176D925DD72B727260DBAAE1FB2F96F
        Point1=ECC_Arithmetic.ECC_multiply_fast(ECC,ECC.G,k)
        r=(e+Point1[0])%ECC.n
        if r==0 or r+k==ECC.n: continue
        s=Algorithm.expand_gcd(1+dA,ECC.n)[1]%ECC.n*(k-r*dA%n)%ECC.n
        if s==0: continue
        r=ECC_code.n2bytes(r)
        s=ECC_code.n2bytes(s)
        return [r,s]
    
def Verify(ECC,Sig,ZA,PA,M):
    """ 
    
    """
    Sig[0]=ECC_code.bytes2n(Sig[0])
    Sig[1]=ECC_code.bytes2n(Sig[1])
    if Sig[0]>n-1 or Sig[0]<1: return False
    if Sig[1]>n-1 or Sig[1]<1: return False
    e=connect(ZA,M)
    e=SM3.SM3(e)
    t=(Sig[0]+Sig[1])%n
    Point=ECC_Arithmetic.ECC_add(ECC,ECC_Arithmetic.ECC_multiply_fast(ECC,ECC.G,Sig[1]),ECC_Arithmetic.ECC_multiply_fast(ECC,PA,t))
    R=(Point[0]+e)%n
    if R==Sig[0]:return True
    else: return False

def connect(a,b):
    """ bytes connection """
    if type(a) is str:
        a=s2n(a)
    if type(b) is str:
        b=s2n(b)
    b_length=math.ceil(b.bit_length()/8)
    return (a<<(b_length*8))|b

if __name__=="__main__":
    p=0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
    a=0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
    b=0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
    xG=0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
    yG=0X0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
    G=[xG,yG]
    n=0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
    M="message digest"
    dA=0x128B2FA8BD433C6C068C8D803DFF79792A519A55171B1B650C23661D15897263
    xP=0x0AE4C7798AA0F119471BEE11825BE46202BB79E2A5844495E97C04FF4DF2548A
    yP=0x7C0240F88F1CD4E16352A73C17B7F16F07353E53A176D684A9FE0C6BB798E857
    PA=[xP,yP]
    ZA=0xF4A38489E32B45B6F876E3AC2168CA392362DC8F23459C1D1146FC3DBFB7BC9A
    ECC1=ECC_Arithmetic.ECC(a,b,p,G,n)
    signature=Sign(ECC1,M,PA,dA,ZA)
    print(hex(ECC_code.bytes2n(signature[0])))
    print(hex(ECC_code.bytes2n(signature[1])))
    print(Verify(ECC1,signature,ZA,PA,M))
    # if k=0x6CB28D99385C175C94F94E934817663FC176D925DD72B727260DBAAE1FB2F96F
    # 0x40f1ec59f793d9f49e09dcef49130d4194f79fb1eed2caa55bacdb49c4e755d1
    # 0x6fc6dac32c5d5cf10c77dfb20f7c2eb667a457872fb09ec56327a67ec7deebe7
    # True