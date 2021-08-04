from tools import n2bytes,bytes2n
import SM3
import ECC_Arithmetic
import random
import math
import ECC_code
from libnum import s2n
def KDF(Z,klen,):#m密钥派生函数
    """ Z--共享的秘密比特串，klen--要获得的密钥数据的比特长度 """
    ct=0x00000001
    Ha=[0]
    K=0
    for i in range(1,math.ceil(klen/256)+1):
        Ha.append(SM3.SM3((Z<<32)|ct))
        ct+=1
    if klen%256==0:
        HAI=Ha[math.ceil(klen/256)]
    else:
        HAI=Ha[math.ceil(klen/256)]>>(256-klen+(256*(klen//256)))
    for i in range(1,math.ceil(klen/256)):
        K<<=256
        K|=Ha[i]
    K<<=256
    K|=HAI
    return K

def encrypt(ECC,M,PB):
    """ ECC--椭圆曲线(包含a,b,p,G,n),M- 要加密的信息 PB-公钥"""
    while(True):
        k=random.randint(1,n-1)
        k=0x384F30353073AEECE7A1654330A96204D37982A3E15B2CB5
        C1=ECC_Arithmetic.ECC_multiply_fast(ECC,ECC.G,k)
        # print(hex(C1[0]),hex(C1[1]))
        C1=ECC_code.point2bytes(C1,1)#未压缩表示
        h=SM3.SM3(M)
        S=ECC_Arithmetic.ECC_multiply_fast(ECC,PB,h)
        if S==[-1,-1]:return False
        Point2=ECC_Arithmetic.ECC_multiply_fast(ECC,PB,k)
        t=KDF((Point2[0]<<192)|Point2[1],len(M)*8)
        # print(hex(t))
        if t!=0: break 
    C2=n2bytes((s2n(M)^t))
    # print(hex(bytes2n(C2)))
    # print(hex(bytes2n(Point2[0].to_bytes(24,'big')+M+Point2[1].to_bytes(24,'big'))))
    C3=(SM3.SM3(Point2[0].to_bytes(24,'big')+M+Point2[1].to_bytes(24,'big')))# x2 || M || y2
    C3=n2bytes(C3)
    # print(hex(bytes2n(C2)))
    return C1+C3+C2

def decrypt(ECC,dB,C):
    """ ECC--椭圆曲线(包含a,b,p,G,n)  dB-私钥  C-密文 """
    C1,C2,C3=apartC(C)
    # print(hex(bytes2n(C1)),hex(bytes2n(C2)),hex(bytes2n(C3)))
    C1=ECC_code.bytes2point(ECC.a,ECC.b,C1,1,p)
    # print(hex(C1[0]),hex(C1[1]))
    if ECC_code.get_y(a,b,p,C1[0])!=C1[1] and (p-ECC_code.get_y(a,b,p,C1[0]))!=C1[1]:
        print("wrong1!")
        return 0
    h=1 ##h是啥...
    S=ECC_Arithmetic.ECC_multiply_fast(ECC,C1,h)
    if S==[-1,-1]:
        print("wrong2!")
        return 0
    Point2=ECC_Arithmetic.ECC_multiply_fast(ECC,C1,dB)
    t=KDF((Point2[0]<<192)|Point2[1],len(C2)*8)
    M=(bytes2n(C2)^t).to_bytes(len(C2),'big')
    u=SM3.SM3(Point2[0].to_bytes(24,'big')+M+Point2[1].to_bytes(24,'big')).to_bytes(32,'big')
    if u!=C3:
        print("wrong3!")
        return 0
    return M

def apartC(C):
    C1=C[:49]
    C3=C[49:81]
    C2=C[81:]
    return C1,C2,C3
if __name__=='__main__':
    p=0xBDB6F4FE3E8B1D9E0DA8C0D46F4C318CEFE4AFE3B6B8551F
    a=0xBB8E5E8FBC115E139FE6A814FE48AAA6F0ADA1AA5DF91985
    b=0x1854BEBDC31B21B7AEFC80AB0ECD10D5B1B3308E6DBF11C1
    xG=0x4AD5F7048DE709AD51236DE65E4D4B482C836DC6E4106640
    yG=0x02BB3a02D4AAADACAE24817A4CA3A1B014B5270432DB27D2
    G=(xG,yG)
    n=0xBDB6F4FE3E8B1D9E0DA8C0D40FC962195DFAE76F56564677
    M=b"encryption standard"
    dB=0x58892B807074F53FBF67288A1DFAA1AC313455FE60355AFD
    xB=0x79F0A9547AC6D100531508B30D30A56536BCFC8149F4AF4A
    yB=0xAE38F2D8890838DF9C19935A65A8BCC8994BC7924672F912
    PB=(xB,yB)
    ECC1=ECC_Arithmetic.ECC(a,b,p,G,n)
    cipher=encrypt(ECC1,M,PB)
    print(hex(bytes2n(cipher)))

    # cipher+=b'\x86'
    print(decrypt(ECC1,dB,cipher))
    # x2=0x57E7B63623FAE5F08CDA468E872A20AFA03DED41BF140377
    # y2=0x0E040DC83AF31A67991F2B01EBF9EFD8881F0A0493000603
    # 0x423fc680b124294dfdf34dbe76e0c38d883de4d41fa0d4cf570cf14f20daf0c4d777f738d16b16824d31eefb9de31ee1f6afb3bcebd76f82b252ce5eb25b5799686902b8cf2fd87536e55ef7603b09e7c610567dbd4854f51f4f00adcc01cfe90b1fb1c
    # b'encryption standard'
    # print(hex(KDF((x2<<192)|y2,152)))