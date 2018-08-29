''' Encrypts message using Vigenere's cipher method '''
import sys
from cs50 import get_string

if len(sys.argv) != 2:
    print("Usage: ./vigenere k")
    sys.exit(1)
else:
    t = list(sys.argv[1])

    for i in range(len(t)):
        if not t[i].isalpha():
            print("Usage: ./vigenere k")
            sys.exit(1)
        else:
            if t[i].isupper():
                t[i] = ord(t[i]) - ord('A')
            else:
                t[i] = ord(t[i]) - ord('a')

    s = get_string("plaintext: ")

    # Constant on character limit
    CHAR_LIM = 26

    m = c = 0
    s = list(s)
    for i in range(len(s)):
        if s[i].isalpha():
            m = c % len(t)
            c += 1

            # Cycle through alphabets -> (t - CHAR_LIM),
            # if the movement of t is as same direction as alphabetical order
            # Same goes for t, like a cycle
            if s[i].isupper():
                if ord(s[i]) + t[m] >= ord('A') + CHAR_LIM:
                    s[i] = chr(ord(s[i]) + t[m] - CHAR_LIM)
                else:
                    s[i] = chr(ord(s[i]) + t[m])
            elif s[i].islower():
                if ord(s[i]) + t[m] >= ord('a') + CHAR_LIM:
                    s[i] = chr(ord(s[i]) + t[m] - CHAR_LIM)
                else:
                    s[i] = chr(ord(s[i]) + t[m])

    print("ciphertext: {}".format(''.join(s)))