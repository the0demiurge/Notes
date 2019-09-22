```c++
#include <cstdio>
#include <iostream>

using namespace std;

class A {
  public:
    A(int i) {
        cout << "construct A int" << endl;
        this->i = i;
    }
    A(void) {
        cout << "construct A void" << endl;
        this->i = 0;
    }
    ~A(void) {
        cout << "destruct A" << endl;
    }
    void f(void) {
        cout << "A.f called" << this->i << endl;
    }

  private:
    int i;
};
class B : public A {
  public:
    B(int i) : A(33) {
        cout << "construct B int" << endl;
        this->i = i;
        // A::f();
    }
    ~B(void) {
        cout << "destruct B" << endl;
    }
    void f(void) {
        cout << "B.f called" << this->i << endl;
    }

  private:
    int i;
};
int main() {
    A *pa = new B(1);
    ((B *)pa)->f();
    pa->f();
    // delete pa;
    B *pb = (B *)pa;
    pb->f();
    delete pb;
    pa = NULL;
    pb = NULL;

    cout << endl;
    B b(2);
    b.f();

    return 0;
}
```

## Results
```
construct A int
construct B int
B.f called1
A.f called33
B.f called1
destruct B
destruct A

construct A int
construct B int
B.f called2
destruct B
destruct A```
