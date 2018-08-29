// Program to get the minimum number of coins for certain change
#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    // No negative cash/change
    float f = -0.1;
    while (f < 0)
    {
        f = get_float("Change owed: ");
    }

    // Conversion to int for calculation
    int change = (int)(roundf(f * 100));

    // Let's make it complicated...
    int quarter = 25, dime = 10, nickel = 5, penny = 1;
    int n = 0;
    while (change > 0)
    {
        change -= change >= quarter ? quarter : (change >= dime ? dime : (change >= nickel ? nickel : (change >= penny ? penny : 0)));
        n++;
    }
    printf("%d\n", n);
}