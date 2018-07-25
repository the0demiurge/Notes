# Vector

使用给定数值初始化

```c++
#include <vector>
vector <T> vec_a {x, y, z};  // c++11
vector <T> vec_a(vec_b);
vector <T> vec_a(vec_b.begin(), vec_b.begin() + length_to_copy);
vector <T> vec_a(array_b, array_b + length_to_copy);
vector <T> vec_a(address_begin, address_end);
```

遍历

```c++
for(auto v: vec) cout << v;  // c++11
/* 迭代器 */
vector <T> :: iterator t;  // t 是指针
for(t = vec.begin(); t != vec.end(); t++) cout << *t;


/* 二维向量 */
vector <vector <int>> vec {{1, 2, 3}, {4, 5}};

for(auto row: vec){  // c++11
    for(auto v: row){
        cout << v << '\t';
    }
    cout << endl;
}

for(int row=0; row < vec.size(); row++){
    for(int col=0; col < vec[row].size(); col++){
        cout << vec[row][col] << '\t';
    }
    cout << endl;
}
```

