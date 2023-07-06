#!/usr/bin/python3
import socket
from binascii import hexlify, unhexlify
from time import sleep

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
    C = oracle.ctext
    cipher_size = len(C)
    plain_size = cipher_size - 16
    P = bytearray(plain_size)
    D = xor(P, C)
    C_copy = bytearray(plain_size)
    
    for k in range(1, 17):
        for i in range(256):
            C_copy[plain_size - k] = i
            if oracle.decrypt(C[:16] + C_copy[16:32] + C[32:]) == "Valid":
                break
        P[plain_size - k] = C[plain_size - k] ^ C_copy[plain_size - k] ^ k
        for j in range(1, k+1):
            C_copy[plain_size - j] = C[plain_size - j] ^ (k + 1) ^ P[plain_size - j]

        # Print the updated P with changed digit in green
#!/usr/bin/python3
import socket
from binascii import hexlify, unhexlify
from time import sleep

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
    C = oracle.ctext
    cipher_size = len(C)
    plain_size = cipher_size - 16
    P = bytearray(plain_size)
    D = xor(P, C)
    C_copy = bytearray(plain_size)
    
    for k in range(1, plain_size + 1):
        for i in range(256):
            C_copy[plain_size - k] = i
            if oracle.decrypt(C[:16] + C_copy[16:32] + C[32:]) == "Valid":
                break
        P[plain_size - k] = C[plain_size - k] ^ C_copy[plain_size - k] ^ k
        for j in range(1, k+1):
            C_copy[plain_size - j] = C[plain_size - j] ^ (k + 1) ^ P[plain_size - j]

        # Print the updated P with changed digit in green
        colored_P = ""
        for index, digit in enumerate(P):
            if digit != 0x00:
                colored_P += bcolors.OKGREEN + f"{digit:02X}" + bcolors.ENDC
            else:
                colored_P += f"{digit:02X}"

        print(f"[PLAIN] {colored_P}\r", end="")
        sleep(0.1)
