// Implement a program that encrypts messages using Caesar’s cipher (integer key)
// stdlib -> atoi, ctype -> islower, isupper, string -> strlen
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
        printf("Usage: ./caesar k\n");

        // FAIL
        return 1;
    }

    // Only 1 argument, PASS
    else
    {
        string s = get_string("plaintext:  ");

        // Key
        int k = atoi(argv[1]);
        // Constant on character limit
        const int CHAR_LIM = 26;

        // Larger than 26? No problem, make it within 26
        if (k >= CHAR_LIM)
        {
            k %= CHAR_LIM;
        }

        for (int i = 0, n = strlen(s); i < n; i++)
        {
            // Cycle through alphabets -> (k - CHAR_LIM), if the movement of k is as same direction as alphabetical order
            if (isupper(s[i]))
            {
                s[i] += (s[i] + k >= 'A' + CHAR_LIM) ? (k - CHAR_LIM) : k;
            }
            else if (islower(s[i]))
            {
                s[i] += (s[i] + k >= 'a' + CHAR_LIM) ? (k - CHAR_LIM) : k;
            }
        }

        printf("ciphertext: %s\n", s);

        // SUCCESS
        return 0;
    }
}