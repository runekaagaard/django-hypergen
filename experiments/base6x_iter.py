import string


def base65_counter():
    # THX: https://stackoverflow.com/a/49710563/164449
    abc = string.letters + string.digits + "-_:"
    base = len(abc)
    i = -1
    while True:
        i += 1
        num = i
        output = abc[num % base]  # rightmost digit

        while num >= base:
            num //= base  # move to next digit to the left
            output = abc[num % base] + output  # this digit

        yield output


c = base65_counter()
for i in range(500):
    print next(c),
