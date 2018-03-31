```c++
#include <iostream>

using namespace std;

int main(int argc, const char* argv[]){
  cout<<"testing argc, argv"<<endl;
  cout<<"argc = "<<argc<<endl;
  for (int i = 0; i < argc; i++) {
    cout<<"i = "<<i<<" argv = "<<argv[i]<<endl;
  }
  return 0;
}
```