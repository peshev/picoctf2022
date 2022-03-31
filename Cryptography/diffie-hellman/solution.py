#!/usr/bin/env python3

alphabet = [chr(ord('A') + i) for i in range(26)] + [chr(ord('0') + i) for i in range(10)]


def caesar(c, key):
    if c in alphabet:
        return alphabet[(alphabet.index(c) - key) % len(alphabet)]
    else:
        return c


p = 13
g = 5

a = 7
b = 3

A = g ** a % p
B = g ** b % p

s = B ** a % p

assert s == A ** b % p

with open("message.txt") as fp:
    ciphertext = fp.read().strip()

flag = "".join(map(lambda x: caesar(x, s), ciphertext))

print(f"picoCTF{{{flag}}}")
