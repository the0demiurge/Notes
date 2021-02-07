def swap_plus_minus(a, b):
    a -= b
    b -= a
    a += b
    b -= a
    b = a - b
    return a, b


def swap_xor(a, b):
    a ^= b
    b ^= a
    a ^= b
    return a, b


a, b = 17, 19
print('a, b', (a, b))
print(swap_plus_minus(a, b))
print(swap_xor(a, b))
