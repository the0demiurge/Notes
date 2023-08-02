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
