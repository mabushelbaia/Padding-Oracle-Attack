#!/usr/bin/python3
import socket
from binascii import hexlify, unhexlify
from time import sleep
from rich.console import (Console, Group)
from rich.progress import (Progress,TextColumn)
from rich.panel import Panel
from rich.live import Live


def xor(first, second):
    return bytearray(x ^ y for x, y in zip(first, second))

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
        self.s.send(hexstr + b"\n")

    def __del__(self):
        self.s.close()


if __name__ == "__main__":
    oracle = PaddingOracle("10.9.0.80", 6000)
    cipher_text = oracle.ctext
    cipher_text = [
        bytearray(cipher_text[i : i + 16]) for i in range(0, len(cipher_text), 16)
    ]
    blocks = len(cipher_text)
    cipher_copy = [bytearray(16) for _ in range(blocks)]
    plain_text = [bytearray(16) for _ in range(blocks - 1)]
    texts_progress = Progress(
        TextColumn("{task.description}"),
    )
    text1_task_id = texts_progress.add_task("[bold blue]PLAIN-HEX:")
    text2_task_id = texts_progress.add_task("[bold blue]PLAIN-TEXT:")
    text3_task_id = texts_progress.add_task("[bold blue]CIPHER-TEXT:")
    overalL_progress = Progress()
    t = overalL_progress.add_task("[bold blue]Decrypting\t\t ", total=(blocks - 1) * 16)
    panel = Panel(Group(texts_progress, overalL_progress), title="Padding Oracle Attack", border_style="bold")
    with Live(panel):
        for j in range(blocks - 2, -1, -1):
            for k in range(1, 16 + 1):
                for i in range(256):
                    cipher_string = " ".join([f.hex() for f in cipher_copy])
                    texts_progress.update(text3_task_id, description=f"[bold blue]CIPHER-HEX:\t [white]{cipher_string}")
                    cipher_copy[j][16 - k] = i
                    cipher = bytearray()
                    for _ in range(j):
                        cipher += cipher_text[_]
                    cipher += cipher_copy[j] + cipher_text[j + 1]
                    if oracle.decrypt(cipher) == "Valid":
                        break
                plain_text[j][16 - k] = cipher_text[j][16 - k] ^ cipher_copy[j][16 - k] ^ k
                plain_hex = " ".join([f.hex() for f in plain_text])
                plain_bytes = b''.join([f for f in plain_text])
                texts_progress.update(text1_task_id, description=f"[bold blue]PLAIN-HEX:\t [white]{plain_hex}")
                if plain_bytes.decode('utf-8', errors='ignore'):
                    texts_progress.update(text2_task_id, description=f"[bold blue]PLAIN-TEXT:\t [white]{plain_bytes.decode('utf-8', errors='ignore')}")
                overalL_progress.update(t, advance=1)
                for l in range(1, k + 1):
                    cipher_copy[j][16 - l] = (
                        cipher_text[j][16 - l] ^ (k + 1) ^ plain_text[j][16 - l]
                    )
                sleep(0.1)