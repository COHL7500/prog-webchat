import math, re, numpy, random, sympy, re

class textConversion:
    def txtToInt(self, txt):
        outputmsg = ""
        for char in txt.lower():
            outputmsg = outputmsg + str(ord(char)+100)
        return int(outputmsg)

    def intToTxt(self, integer):
        outputmsg = ""
        integer = re.findall("...", str(integer))
        for char in integer:
            char = chr(int(char) - 100)
            outputmsg = outputmsg + char
        return outputmsg

class RSA:
    def __init__(self):
        self.txtconv = textConversion()

    def encrypt(self, m, publicKey):
        m = self.txtconv.txtToInt(m)
        return pow(m, publicKey[0], publicKey[1])

    def decrypt(self, c):
        return self.txtconv.intToTxt(pow(c, self.getPrivateKey()[0], self.getPrivateKey()[1]))

    def getPublicKey(self):
        return self.e, self.n

    def getPrivateKey(self):
        return self.d, self.n 

    def genKey(self):
        p = self.randPrime(768)
        q = self.randPrime(1280)

        self.n = p * q
        phi = (p - 1) * (q - 1)
        
        self.e = 65537
        self.d = self.modInv(self.e, phi) 

    def egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def randPrime(self, bits):
        p_candidate = random.getrandbits(bits)
        while not sympy.isprime(p_candidate):
            p_candidate = sympy.nextprime(p_candidate)
            if p_candidate.bit_length() < bits:
                p_candidate = random.getrandbits(bits)
        return p_candidate


    def modInv(self, a, m):
        g, x, y = self.egcd(a, m)
        if g != 1:
            return None
        else:
            return x % m


txtc = textConversion()
rsa = RSA()

rsa.genKey()
txt = "hallo my guys, dude 123412"
print("plaintext: ", txt)

key = rsa.getPublicKey()

d = rsa.encrypt(txt, key)
print("cipher text: ", d)


e = rsa.decrypt(d)
print("plaintext: ",e)
