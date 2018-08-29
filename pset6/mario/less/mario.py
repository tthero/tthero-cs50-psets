# Mario program - Less comfortable
from cs50 import get_int

while True:
    # Height, h and initialise it
    h = get_int("Height: ")
    if h >= 0 and h <= 23:
        break

# For loop on displaying the result
for i in range(1, h + 1):
    for j in range(h, 0, -1):
        print(" " if j > i else "#", end="")
    print("#")