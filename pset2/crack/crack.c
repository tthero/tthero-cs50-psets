// Implement a program to decipher a certain code
// Required headers
// This definition is most likely to make use of some extra functions that are defined in the X/Open and POSIX standards.
#define _XOPEN_SOURCE
#include <unistd.h>

#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

#define DES_SIZE 2
#define PW_LIMIT 5

// The struct for cracking
typedef struct crackTool
{
    char *seed;
    unsigned int seedNum;
    unsigned int alphaStart;
    char salt[DES_SIZE];
}
cracker;

// Prototyping
// Uses cracker *c so that we can directly change the value inside struct
bool cracking(string s, string res, cracker *c, int n);

int main(int argc, string argv[])
{
    // No or more than 1 argument, FAIL
    if (argc != 2)
    {
        printf("Usage: ./crack hash\n");

        // FAIL
        return 1;
    }

    // Only 1 argument, PASS
    else
    {
        // DES-based cryptography
        // Thus, no need to put $(ID)$...... in salt
        char *s = argv[1];

        printf("Before: %s\n", s);

        cracker c;

        c.seed = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
        c.seedNum = strlen(c.seed);
        c.alphaStart = 12;

        // DES salt = first 2 characters of the string
        for (int i = 0; i < DES_SIZE; i++)
        {
            // Apparently, another way of displaying specific character for a string (s[i]) is *(string + i)
            // *(string) is referring to first address of array, which is first character of string
            // *(string + i) will be address plus i, thus becomes i-th character of string
            c.salt[i] = *(s + i);
        }

        // Assume password limit is 5 characters and within A-Z and a-z
        // Outermost loop will be the last character (5th)
        // Innermost loop will be the first character (1st)
        string res;

        for (int i = 0; i < PW_LIMIT; i++)
        {
            // Allocate memory for size of i * char
            res = (string)malloc(i * sizeof(char));

            // Initiate password cracking
            // If true, give me the password, stop password cracking
            if (cracking(s, res, &c, i))
            {
                s = res;
                break;
            }

            free(res);
        }

        printf("After: %s\n", s);

        free(res);
    }
    // SUCCESS
    return 0;
}

bool cracking(string s, string res, cracker *c, int n)
{
    for (int a = c->alphaStart; a < c->seedNum; a++)
    {
        res[n] = c->seed[a];
        if (n - 1 >= 0)
        {
            if (cracking(s, res, c, n - 1))
            {
                return true;
            }
        }
        else
        {
            if (strcmp(s, crypt(res, c->salt)) == 0)
            {
                return true;
            }
        }
    }
    return false;
}