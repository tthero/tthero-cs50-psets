# Encrypts message using Caesar's cipher method
import sys
from cs50 import get_string

if len(sys.argv) != 2:
    print("Usage: ./caesar k")
    sys.exit(1)
else:
    s = get_string("plaintext:  ")

    # Key
    k = int(sys.argv[1])

    # Constant on character limit
    CHAR_LIM = 26

    # Larger than 26? No problem, make it within 26
    if k >= CHAR_LIM:
        k %= CHAR_LIM

    s = list(s)
    for i in range(len(s)):
        if s[i].isupper():
            if ord(s[i]) + k >= ord('A') + CHAR_LIM:
                s[i] = chr(ord(s[i]) + k - CHAR_LIM)
            else:
                s[i] = chr(ord(s[i]) + k)
        elif s[i].islower():
            if ord(s[i]) + k >= ord('a') + CHAR_LIM:
                s[i] = chr(ord(s[i]) + k - CHAR_LIM)
            else:
                s[i] = chr(ord(s[i]) + k)

    print("ciphertext: {}".format(''.join(s)))