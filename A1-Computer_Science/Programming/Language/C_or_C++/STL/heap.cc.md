```C++
#include <algorithm>
#include <functional>
#include <iostream>
#include <vector>
using namespace std;

namespace show {

template <typename T>
void show(vector<T> data, bool ln = true) {
    cout << '[';
    for (auto item : data) cout << item << ", ";
    cout << ']';
    if (ln) cout << endl;
}

}  // namespace show

namespace algorithm {

template <typename T>
class Heap {
  protected:
    function<bool(T, T)> compare;

  public:
    vector<T> data;
    Heap(function<bool(T, T)> compare = less<T>()) : compare(compare) {}
    Heap(initializer_list<T> data, function<bool(T, T)> compare = less<T>()) : data(data), compare(compare) { this->heapify(); }
    Heap(vector<T> data, function<bool(T, T)> compare = less<T>()) : data(data), compare(compare) { this->heapify(); }

    void heapify(void) { make_heap(this->data.begin(), this->data.end(), this->compare); }
    void push(const T& value) {
        this->data.push_back(value);
        push_heap(this->data.begin(), this->data.end(), this->compare);
    }
    const T pop() {
        T top = this->top();
        pop_heap(this->data.begin(), this->data.end(), this->compare);
        this->data.pop_back();
        return top;
    }
    const T top() {
        if (this->size() > 0) {
            return this->data[0];
        } else {
            throw out_of_range("Pop from an empty heap");
        }
    }
    const int size() { return this->data.size(); }
};
}  // namespace algorithm

int main() {
    algorithm::Heap<int> heap{6, 1, 2, 5, 3, 4};

    cout << "heaped: ";
    show::show(heap.data);

    heap.push(100);
    heap.push(43);
    heap.push(10);
    heap.push(20);

    cout << "pushed: ";
    show::show(heap.data);

    for (int i = 0; i < 8; i++) {
        cout << heap.pop();
        show::show(heap.data);
    }
    return 0;
}

```

