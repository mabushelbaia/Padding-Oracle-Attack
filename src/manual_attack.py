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
    IV, C1, C2 = oracle.ctext[:16], oracle.ctext[16:32], oracle.ctext[32:48]
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
    
    print(f"[{len(IV)} Bytes] IV:  {IV.hex()}")
    print(f"[{len(C1)} Bytes] C1:  {C1.hex()}")
    print(f"[{len(C2)} Bytes] C2:  {C2.hex()}")        
    print(f"[{len(P)//2} Bytes] P1:  {P[00:16].hex()}")
    print(f"[{len(P)//2} Bytes] P2:  {P[16:32].hex()}")
    