#!/usr/bin/python3
import socket
from binascii import hexlify, unhexlify
from time import sleep
from colors import bcolors

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
    oracle = PaddingOracle('10.9.0.80', 6000)
    cipher_text = oracle.ctext
    cipher_text = [bytearray(cipher_text[i:i+16]) for i in range(0, len(cipher_text), 16)]
    blocks = len(cipher_text)
    cipher_copy = [bytearray(16) for _ in range(blocks)]
    plain_text = [bytearray(16) for _ in range(blocks - 1)]
    for j in range(blocks-2, -1, -1):
        for k in range (1, 16 + 1):
            for i in range(256):
                cipher_copy[j][16 - k] = i
                cipher = bytearray()
                for _ in range (j):
                    cipher += cipher_text[_]
                cipher += cipher_copy[j] + cipher_text[j+1]
                if oracle.decrypt(cipher) == "Valid":
                    break
            plain_text[j][16 - k] = cipher_text[j][16 - k] ^ cipher_copy[j][16 - k] ^ k
            for l in range(1, k+1):
                cipher_copy[j][16 - l] = cipher_text[j][16 - l] ^ (k + 1) ^ plain_text[j][16 - l]
            colored_P = ""
            for _ in range(len(plain_text)):
                for index, digit in enumerate(plain_text[_]):
                    if digit != 0x00:
                        colored_P += bcolors.OKGREEN + f"{digit:02X}" + bcolors.RESET
                    else:
                        colored_P += f"{digit:02X}"
            print(f"[{bcolors.OKCYAN}{bcolors.BOLD}PLAIN-HEX{bcolors.RESET}] {colored_P}\r", end="")
            sleep(0.1)
    print()
    plain_text = b''.join(plain_text)
    try:
        decoded_text = plain_text.decode('utf-8')
        print(f"[{bcolors.OKCYAN}{bcolors.BOLD}PLAIN-TEXT{bcolors.RESET}] {decoded_text}")
    except UnicodeDecodeError:
        pass