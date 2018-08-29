// Mario program - More comfortable
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

    // Declaring j and mode variables
    int j, mode;

    // For loop on displaying the result
    for (int i = 1; i <= h; i++)
    {
        mode = 1;
        while (mode <= 2)
        {
            j = h;
            while (j > 0)
            {
                // Custom conditions to check what state it is in
                // to output required results
                if (mode == 1)
                {
                    printf(j > i ? " " : "#");
                }
                else
                {
                    printf(j > h - i ? "#" : "");
                }
                j--;
            }
            printf(mode == 1 ? "  " : "\n");
            mode++;
        }
    }
}