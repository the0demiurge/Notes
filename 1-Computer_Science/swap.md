```python
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
```

```C++
#include <iostream>

template <class T>
void swap_plus_minus(T& a, T& b) {
    a -= b;
    b -= a;
    a += b;
    b -= a;
    b = a - b;
}

template <class T>
void swap_xor(T& a, T& b) {
    a ^= b;
    b ^= a;
    a ^= b;
}

int main() {
    int a = 17.2, b = 19.4;
    swap_plus_minus(a, b);
    std::cout << a << ' ' << b << std::endl;
    swap_xor(a, b);
    std::cout << a << ' ' << b << std::endl;
    return 0;
}
```
