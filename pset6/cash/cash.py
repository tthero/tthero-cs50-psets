# Program to get the minimum number of coins for certain change
from cs50 import get_float

while True:
    f = get_float("Change owed: ")
    # No negative cash/change
    if f >= 0:
        break

change = int(f * 100)

# Get number of coins
quarter, dime, nickel, penny, n = 25, 10, 5, 1, 0
while change > 0:
    change -= quarter if change >= quarter else (
        dime if change >= dime else (
            nickel if change >= nickel else (
                penny if change >= penny else 0)))
    n += 1
print(n)