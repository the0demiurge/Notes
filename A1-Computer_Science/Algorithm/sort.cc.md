# Sort in C++

## MergeSort

```c++
#include <iostream>
#include <vector>

using namespace std;

namespace show {
template <typename T>
void show(vector<T> data, bool ln = true) {
    cout << '[';
    for (auto i : data) cout << i << ", ";
    cout << ']';
    if (ln) cout << endl;
}
}  // namespace show

namespace algorithm {
template <typename T>
vector<T> merge(const vector<T>& arr1, const vector<T> arr2) {
    vector<T> result;
    int i = 0, j = 0;
    while (i < arr1.size() && j < arr2.size()) {
        if (arr1[i] <= arr2[j]) {
            result.push_back(arr1[i++]);
        } else {
            result.push_back(arr2[j++]);
        }
    }
    while (i < arr1.size()) result.push_back(arr1[i++]);
    while (j < arr2.size()) result.push_back(arr2[j++]);

    return result;
}
template <typename T>
vector<T> mergesort(const vector<T>& arr, int lo = 0, int hi = -1) {
    if (hi == -1) hi = arr.size();
    if (hi - lo <= 1) return arr;
    int mid = (hi + lo) / 2;
    vector<T> left(arr.begin() + lo, arr.begin() + mid), right(arr.begin() + mid, arr.begin() + hi);
    vector<T> sorted_left = mergesort(left), sorted_right = mergesort(right);
    return merge(sorted_left, sorted_right);
}
}  // namespace algorithm

int main() {
    vector<int> arr{9, 8, 1, 5, 3, 4, 4, 9};
    show::show(arr);
    show::show(algorithm::mergesort(arr));
    return 0;
}

```

Result:

```
[9, 8, 1, 5, 3, 4, 4, 9, ]
[1, 3, 4, 4, 5, 8, 9, 9, ]
```

