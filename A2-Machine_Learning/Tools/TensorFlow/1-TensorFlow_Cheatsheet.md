# 常用功能

## tf.train.get_or_create_global_step(graph=None)

## tf.set_random_seed(seed)

## 异常检测

### tf.check_numerics(tensor, message, name=None)

```python
'''
Checks a tensor for NaN and Inf values.

When run, reports an `InvalidArgument` error if `tensor` has any values
that are not a number (NaN) or infinity (Inf). Otherwise, passes `tensor` as-is.

Args:
  tensor: A `Tensor`. Must be one of the following types: `half`, `bfloat16`, `float32`, `float64`.
  message: A `string`. Prefix of the error message.
  name: A name for the operation (optional).

Returns:
  A `Tensor`. Has the same type as `tensor`.
'''
```

### tf.Assert(condition, data, summarize=None, name=None)

```python
# Ensure maximum element of x is smaller or equal to 1
assert_op = tf.Assert(tf.less_equal(tf.reduce_max(x), 1.), [x])
with tf.control_dependencies([assert_op]):
  ... code using x ...
'''
Args:
  condition: The condition to evaluate.
  data: The tensors to print out when condition is false.
  summarize: Print this many entries of each tensor.
  name: A name for this operation (optional).

Returns:
  assert_op: An `Operation` that, when executed, raises a
  `tf.errors.InvalidArgumentError` if `condition` is not true.
  @compatibility{eager} returns None.

Raises:
  @compatibility{eager} `tf.errors.InvalidArgumentError` if `condition`
  is not true
'''
```

### tf.Print(input_, data, message=None, first_n=None, summarize=None, name=None)

```python
'''
Prints a list of tensors.

This is an identity op (behaves like `tf.identity`) with the side effect
of printing `data` when evaluating.

Note: This op prints to the standard error. It is not currently compatible
  with jupyter notebook (printing to the notebook *server's* output, not into
  the notebook).

Args:
  input_: A tensor passed through this op.
  data: A list of tensors to print out when op is evaluated.
  message: A string, prefix of the error message.
  first_n: Only log `first_n` number of times. Negative numbers log always;
           this is the default.
  summarize: Only print this many entries of each tensor. If None, then a
             maximum of 3 elements are printed per input tensor.
  name: A name for the operation (optional).

Returns:
  A `Tensor`. Has the same type and contents as `input_`.
'''
```

## 自动设定参数

### slim.arg_scope(list_ops_or_scope, **kwargs)

```python
'''
Args:
  list_ops_or_scope: List or tuple of operations to set argument scope for or
    a dictionary containing the current scope. When list_ops_or_scope is a
    dict, kwargs must be empty. When list_ops_or_scope is a list or tuple,
    then every op in it need to be decorated with @add_arg_scope to work.
  **kwargs: keyword=value that will define the defaults for each op in
            list_ops. All the ops need to accept the given set of arguments.

Yields:
  the current_scope, which is a dictionary of {op: {arg: value}}
Raises:
  TypeError: if list_ops is not a list or a tuple.
  ValueError: if any op in list_ops has not be decorated with @add_arg_scope.
'''
```
## 滑动平均

```python
tf.train.ExponentialMovingAverage(decay, num_updates=None, zero_debias=False, name='ExponentialMovingAverage')
'''
Args:
  decay: Float.  The decay to use.
  num_updates: Optional count of number of updates applied to variables.
  zero_debias: If `True`, zero debias moving-averages that are initialized
    with tensors.
  name: String. Optional prefix name to use for the name of ops added in
    `apply()`.
'''
```
# 变量管理

## 类型转换

### tf.cast(x, dtype, name=None)

```python
x = tf.constant([1.8, 2.2], dtype=tf.float32)
tf.cast(x, tf.int32)  # [1, 2], dtype=tf.int32
```

###  tf.convert_to_tensor(value, dtype=None, name=None, preferred_dtype=None)

```python
import numpy as np

def my_func(arg):
  arg = tf.convert_to_tensor(arg, dtype=tf.float32)
  return tf.matmul(arg, arg) + arg

# The following calls are equivalent.
value_1 = my_func(tf.constant([[1.0, 2.0], [3.0, 4.0]]))
value_2 = my_func([[1.0, 2.0], [3.0, 4.0]])
value_3 = my_func(np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32))
```
## Scopes

特点：

- 唯一的区别在于 tf.get_variable 得到的变量名称
- _get_variable 在任何 scope 下均不会 rotate 变量名称，tf.Variable 一直都会 rotate 变量名称
- scope 的 reuse 参数通常用于联系训练模型与测试模型，尤其在于两个模型有差异却共享参数时

### NameScope

```python
with tf.names_cope('name'):
    a = tf.Variable(1, name='a')	# 'name_i/a'	自动 rotate 名称
    b = tf.get_variable('b', ...)	# 'b'	名字固定
```

### VariableScope

```python
with tf.variable_cope('name'):
    a = tf.Variable(1, name='a')	# 'name_i/a'	自动 rotate 名称
    b = tf.get_variable('b', ...)	# 'name/b'	名字固定
```