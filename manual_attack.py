#!/usr/bin/python3
import socket
from binascii import hexlify, unhexlify

# XOR two bytearrays
def xor(first, second):
   return bytearray(x^y for x,y in zip(first, second))

class PaddingOracle:

    def __init__(self, host, port) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

        ciphertext = self.s.recv(4096).decode().strip()
        self.ctext = unhexlify(ciphertext)

    def decrypt(self, ctext: bytes) -> None:
        self._send(hexlify(ctext))
        return self._recv()

    def _recv(self):
        resp = self.s.recv(4096).decode().strip()
        return resp 

    def _send(self, hexstr: bytes):
        self.s.send(hexstr + b'\n')

    def __del__(self):
        self.s.close()


if __name__ == "__main__":
    oracle = PaddingOracle('10.9.0.80', 5000)

    # Get the IV + Ciphertext from the oracle
    iv_and_ctext = bytearray(oracle.ctext)
    IV    = iv_and_ctext[00:16]
    C1    = iv_and_ctext[16:32]  # 1st block of ciphertext
    C2    = iv_and_ctext[32:48]  # 2nd block of ciphertext
    print(f"[{len(IV)} Bytes] IV:  {IV.hex()}")
    print(f"[{len(C1)} Bytes] C1:  {C1.hex()}")
    print(f"[{len(C2)} Bytes] C2:  {C2.hex()}")
    P = bytearray(32)
    C1_copy, IV_copy = bytearray(16), bytearray(16)
    
    for k in range(1, 17):
        for i in range(256):
            C1_copy[16 - k] = i
            status = oracle.decrypt(IV + C1_copy + C2)
            if status == "Valid":
                break

        P[32 - k] = C1_copy[16 - k] ^ C1[16 - k] ^ k
        for j in range(1, k+1):
            C1_copy[16 - j] = C1[16 - j] ^ (k + 1) ^ P[32 - j]
        
        for i in range(256):
            IV_copy[16 - k] = i
            status = oracle.decrypt(IV_copy + C1)
            if status == "Valid":
                break
        P[16 - k] = IV_copy[16 - k] ^ IV[16 - k] ^ k
        for j in range(1, k+1):
            IV_copy[16 - j] = IV[16 - j] ^ (k + 1) ^ P[16 - j]
    print(f"[{len(P)//2} Bytes] P1:  {P[00:16].hex()}")
    print(f"[{len(P)//2} Bytes] P2:  {P[16:32].hex()}")
    
    
    
###############################################################
    # Here, we initialize D2 with C1, so when they are XOR-ed,
    # The result is 0. This is not required for the attack.
    # Its sole purpose is to make the printout look neat.
    # In the experiment, we will iteratively replace these values.
    ###############################################################
    # In the experiment, we need to iteratively modify CC1
    # We will send this CC1 to the oracle, and see its response.
      ###############################################################
    # In each iteration, we focus on one byte of CC1.  
    # We will try all 256 possible values, and send the constructed
    # ciphertext CC1 + C2 (plus the IV) to the oracle, and see 
    # which value makes the padding valid. 
    # As long as our construction is correct, there will be 
    # one valid value. This value helps us get one byte of D2. 
    # Repeating the method for 16 times, we get all the 16 bytes of D2.

    # K = 1
    # for i in range(256):
    #       CC1[16 - K] = i
    #       status = oracle.decrypt(IV + CC1 + C2)
    #       if status == "Valid":
    #           print("Valid: i = 0x{:02x}".format(i))
    #           print("CC1: " + CC1.hex())
    #           break
    # ###############################################################
    # # Once you get all the 16 bytes of D2, you can easily get P2
    # P[15] = CC1[15] ^ D2[15] ^ 0x01
    # CC1[15] = D2[15] ^ 0x02 ^ P[15]
    # print(f"[{len(P)} Bytes] P: {P.hex()}")
    # k = 2   
    # for i in range(256):
    #     CC1[16 - k] = i
    #     status = oracle.decrypt(IV + CC1 + C2)
    #     if status == "Valid":
    #         print("Valid: i = 0x{:02x}".format(i))
    #         print("CC1: " + CC1.hex())
    #         break
    # P[14] = CC1[14] ^ D2[14] ^ 0x02
    # CC1[15] = D2[15] ^ 0x03 ^ P[15]
    # CC1[14] = D2[14] ^ 0x03 ^ P[14]
    # print(f"[{len(P)} Bytes] P: {P.hex()}")
    # k = 3
    # for i in range(256):
    #     CC1[16 - k] = i
    #     status = oracle.decrypt(IV + CC1 + C2)
    #     if status == "Valid":
    #         print("Valid: i = 0x{:02x}".format(i))
    #         print("CC1: " + CC1.hex())
    #         break
    # P[13] = CC1[13] ^ D2[13] ^ 0x03
    # CC1[15] = D2[15] ^ 0x04 ^ P[15]
    # CC1[14] = D2[14] ^ 0x04 ^ P[14]
    # CC1[13] = D2[13] ^ 0x04 ^ P[13]
    # print(f"[{len(P)} Bytes] P: {P.hex()}")
    # k = 4
    # for i in range(256):
    #     CC1[16 - k] = i
    #     status = oracle.decrypt(IV + CC1 + C2)
    #     if status == "Valid":
    #         print("Valid: i = 0x{:02x}".format(i))
    #         print("CC1: " + CC1.hex())
    #         break
    # P[12] = CC1[12] ^ D2[12] ^ 0x04
    # print(f"[{len(P)} Bytes] P: {P.hex()}")
    
