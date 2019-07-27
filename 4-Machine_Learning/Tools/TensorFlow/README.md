### 列举所有本地设备
from [tensorflow github](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/client/device_lib_test.py)
```python
>>> from tensorflow.python.client import device_lib
>>> device_lib.list_local_devices()

[name: "/cpu:0"
 device_type: "CPU"
 memory_limit: 268435456
 locality {
 }
 incarnation: 958941086745573894]
```
### 什么也不做的 op
```python
>>> help(tf.identity)

identity(input, name=None)
    Return a tensor with the same shape and contents as the input tensor or value.
    
    Args:
      input: A `Tensor`.
      name: A name for the operation (optional).
    
    Returns:
      A `Tensor`. Has the same type as `input`.
```


