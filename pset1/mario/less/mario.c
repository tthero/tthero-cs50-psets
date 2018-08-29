// Mario program - Less comfortable
#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Height, h and initialise it
    int h = -1;
    while (h < 0 || h > 23)
    {
        h = get_int("Height: ");
    }

    // For loop on displaying the result
    for (int i = 1; i <= h; i++)
    {
        for (int j = h; j >= 1; j--)
        {
            if (j > i)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        printf("#\n");
    }
}