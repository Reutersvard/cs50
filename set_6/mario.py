from cs50 import get_int

while True:
    h = get_int("Height: ")     # get height from user thanks to get_int
    if h > 0 and h < 9:     # check height between 1 and 8
        break

for i in range(h):
    print(" " * (h - 1 - i) + "#" * (i + 1) + "  " + "#" * (i + 1))     # print the two pyramids