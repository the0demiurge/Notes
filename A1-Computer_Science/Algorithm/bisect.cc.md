# [Bisect in C++](https://github.com/python/cpython/blob/3.6/Lib/bisect.py)

```C++
#include <iostream>
#include <vector>

using namespace std;

namespace algorithm {

template <typename T>
int bisect_right(const vector<T>& arr, const T& value) {
    int lo = 0, hi = arr.size(), mid;
    while (lo < hi) {
        mid = (lo + hi) / 2;
        if (arr[mid] <= value)
            lo = mid + 1;
        else
            hi = mid;
    }
    return lo - 1;
}

template <typename T>
int bisect_left(const vector<T>& arr, const T& value) {
    int lo = 0, hi = arr.size(), mid;
    while (lo < hi) {
        mid = (lo + hi) / 2;
        if (arr[mid] < value) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

template <typename T>
int bisect_right_rev(const vector<int>& arr, const T& value) {
    int lo = 0, hi = arr.size(), mid;
    while (lo < hi) {
        mid = (lo + hi) / 2;
        if (value <= arr[mid])
            lo = mid + 1;
        else
            hi = mid;
    }
    return lo - 1;
}

template <typename T>
int bisect_left_rev(const vector<int>& arr, const T& value) {
    int lo = 0, hi = arr.size(), mid;
    while (lo < hi) {
        mid = (lo + hi) / 2;
        if (value < arr[mid])
            lo = mid + 1;
        else
            hi = mid;
    }
    return lo;
}

}  // namespace algorithm

int main() {
    vector<int> arr{5, 4, 4, 4, 4, 4, 1};
    cout << algorithm::bisect_left_rev(arr, 4) << endl;
}
```
