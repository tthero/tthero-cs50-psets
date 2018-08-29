# Implement a program to decipher a certain code
# Importing functions from builtins
import sys
import crypt


def main():
    # Main function
    global s, alpha_start, seed, seed_num, salt
    if len(sys.argv) != 2:
        print("Usage: ./crack hash")
        sys.exit(1)
    else:
        s = sys.argv[1]
        print("Before: {}".format(s))

        seed = list("./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        seed_num = len(seed)
        alpha_start = 12
        cracked = False

        salt = s[:2]

        res = []
        for i in range(5):
            res.append(seed[alpha_start])
            if cracking(res, i):
                break

        print("After: {}".format(''.join(res)))


def cracking(res, i):
    # Password cracking function
    for j in range(alpha_start, seed_num):
        res[i] = seed[j]
        if i - 1 >= 0:
            if cracking(res, i - 1):
                return True
        else:
            # Main recipe for this program: crypt.crypt(word, salt)
            if s == crypt.crypt(''.join(res), salt):
                return True
    return False


# Declaring module name?
if __name__ == "__main__":
    main()