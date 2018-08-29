// Implement a program that encrypts messages using Vigenere’s cipher (char2int key)
// ctype -> islower, isupper, string -> strlen
#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
    // No or more than 1 argument, FAIL
    if (argc != 2)
    {
        printf("Usage: ./vigenere k\n");

        // FAIL
        return 1;
    }

    // Only 1 argument, PASS
    else
    {
        // Key will be only alphabets, strictly no other elements, including numbers
        string t = argv[1];
        int k[strlen(t)];

        for (int i = 0, n = strlen(t); i < n; i++)
        {
            if (isalpha(t[i]) == 0)
            {
                printf("Usage: ./vigenere k\n");

                // FAIL
                return 1;
            }
            else
            {
                k[i] = isupper(t[i]) ? (int)(t[i] - 'A') : (int)(t[i] - 'a');
            }
        }

        string s = get_string("plaintext:  ");
        // Constant on character limit
        const int CHAR_LIM = 26;

        for (int i = 0, n = strlen(s), m = 0, counter = 0; i < n; i++)
        {
            // Cycle through alphabets -> (k - CHAR_LIM), if the movement of k is as same direction as alphabetical order
            // Same goes for k, like a cycle
            if (isalpha(s[i]))
            {
                // m and counter because if other non-alpha chars exist, the number is skipped to
                // next char (if that is alpha char)
                m = counter++ % strlen(t);

                if (isupper(s[i]))
                {
                    s[i] += (s[i] + k[m] >= 'A' + CHAR_LIM) ? (k[m] - CHAR_LIM) : k[m];
                }
                else if (islower(s[i]))
                {
                    s[i] += (s[i] + k[m] >= 'a' + CHAR_LIM) ? (k[m] - CHAR_LIM) : k[m];
                }
            }
        }

        printf("ciphertext: %s\n", s);

        // SUCCESS
        return 0;
    }
}