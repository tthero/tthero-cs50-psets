// Program to verify the credit card number
#include <stdio.h>
#include <cs50.h>

int main(void)
{
    long long card = get_long_long("Number: ");
    // The d is to make multiplication with 2 more neat, n is numbers of digit, r is remainder, sum is sum...
    int i = 0, d = 0, n = 0, r = 0, sum = 0;
    // The result? AMEX, MASTERCARD, VISA, INVALID?
    int result = 0;

    while (card > 0)
    {
        r = (int)(card % 10);
        card /= 10;

        if (i == 0)
        {
            sum += r;
            i = 1;
        }
        else
        {
            d = r * 2;
            sum += (d >= 10) ? (d / 10) + (d % 10) : d;
            i = 0;
        }
        n++;

        // Verifying if this card is AMEX, MASTERCARD or VISA (must be more than 12 digits)
        // AMEX (A), MASTERCARD (M), VISA (V)
        if (n >= 13)
        {
            if (card < 10)
            {
                // 2nd digit
                if (card > 0)
                {
                    // SPECIAL CASE
                    if (r > 0 && r < 6)
                    {
                        // A, M, V or M, V
                        result = (r == 4) ? 9 : 8;
                    }
                    // A or V
                    else if (r > 6 && r < 8)
                    {
                        result = 7;
                    }
                    // V
                    else
                    {
                        result = 3;
                    }
                }
                // 1st digit
                else
                {
                    // A, V
                    if (result == 7)
                    {
                        result = r == 3 ? 1 : (r == 4 ? 3 : 0);
                    }
                    // M, V
                    else if (result == 8)
                    {
                        result = r == 5 ? 2 : (r == 4 ? 3 : 0);
                    }
                    // A, M, V
                    else if (result == 9)
                    {
                        result = r == 3 ? 1 : (r == 4 ? 3 : (r == 5 ? 2 : 0));
                    }
                    // VISA
                    else
                    {
                        if (r != 4)
                        {
                            result = 0;
                        }
                    }

                    // Check the 1st digit of sum in the end
                    if (sum % 10 != 0)
                    {
                        result = 0;
                    }
                }
            }
        }
    }

    // Prints result == 1 -> AMEX, result == 2 -> MASTERCARD, result == 3 -> VISA
    printf(result == 1 ? "AMEX\n" : (result == 2 ? "MASTERCARD\n" : (result == 3 ? "VISA\n" : "INVALID\n")));
}