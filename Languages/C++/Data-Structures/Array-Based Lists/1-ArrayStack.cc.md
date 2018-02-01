```c++
#include <iostream>

using namespace std;

template <class T> class ArrayStack{
public:
  T* self_data;
  int n = 0;

  ArrayStack(T* data, int n){
    T* d;
    for(int i=0; i < n; i++){d[i] = data[i];}
    delete self_data;
    self_data = d;
    this->n = n;
  }

  void print(){
  }
};

int main(void) {
  string data[] = {"asdf", "wert"};
  ArrayStack <char> a(data, 2);
  //a(data, 5);
  return 0;
}
```