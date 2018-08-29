# Implements credit card number verification program
from cs50 import get_int

# Get number, nice, Python supports more range of number than we thought
card = get_int("Number: ")

# i to alternate odd and even, d is to make times 2 neater, n is number of digits
# r is remainder, s is sum, result is result...
i = d = n = r = s = result = 0

while (card > 0):
    r = card % 10
    card //= 10

    if i == 0:
        s += r
        i = 1
    else:
        d = r * 2
        s += (d // 10) + (d % 10) if d >= 10 else d
        i = 0
    n += 1

    # Verifying if this card is AMEX, MASTERCARD or VISA (must be more than
    # 12 digits)
    # AMEX (A), MASTERCARD (M), VISA (V)
    if n >= 13:
        if card < 10:
            # 2nd digit
            if card > 0:
                # SPECIAL CASE:
                # A, M, V or M, V
                if (r > 0 and r < 6):
                    result = 9 if r == 4 else 8
                # A, V
                elif (r > 6 and r < 8):
                    result = 7
                # VISA
                else:
                    result = 3
            # 1st digit
            else:
                # A, V
                if result == 7:
                    result = 1 if r == 3 else (3 if r == 4 else 0)
                # M, V
                elif result == 8:
                    result = 2 if r == 5 else (3 if r == 4 else 0)
                # A, M, V
                elif result == 9:
                    result = 1 if r == 3 else (3 if r == 4 else (
                        2 if r == 5 else 0))
                # VISA
                else:
                    if r != 4:
                        result = 0

                # Check the 1st digit of sum in the end
                if s % 10 != 0:
                    result = 0

choice = ("INVALID", "AMEX", "MASTERCARD", "VISA")
print(choice[result])