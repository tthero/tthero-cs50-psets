# Mario program - more comfortable
from cs50 import get_int

while True:
    h = get_int("Height: ")
    if h >= 0 and h <= 23:
        break

# Declaring j and mode variables
j = mode = 0

# For loop on displaying the result
for i in range(1, h + 1):
    mode = 0
    while mode <= 1:
        j = h
        while j > 0:
            # Custom conditions to check what state it is in
            # to output required results
            if mode == 0:
                print(" " if j > i else "#", end="")
            else:
                print("#" if j > h - i else "", end="")
            j -= 1
        print("  " if mode == 0 else "\n", end="")
        mode += 1