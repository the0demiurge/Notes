# Attention

复习一下上一篇文章，现有一组数据集$(x_i, y_i)$，其中$x_i$作为key, $y_i$作为value，对于新来的$x$作为query，估计$y$，就是attention的基本模型。对于一个窗口内的全部$(x_y, y_i)$，可以通过加权的方式估计$y$：
$$
\hat{y}=\sum\limits_i\alpha(x,x_i)y_i
$$
其中，$\alpha(x, x_i)$就可以看作attention。注意到上一篇的注意力权重为：
$$
f(x)=\sum\limits_isoftmax\left(-\frac{1}{2}\left((x-x_i)w\right)^2\right)y_i
$$
可以单独把softmax的输入抽象出来，作为注意力评分函数，有：
$$
\begin{array}{rcl}
f(x)&=&\sum\limits_isoftmax\left(a(x,x_i)\right)y_i\\
a(x,x_i)&=&-\frac{1}{2}\left((x-x_i)w\right)^2
\end{array}
$$
后面各种attention只需要在注意力评分函数$a(x,x_i)$上面做文章即可。注意力评分函数$a(\mathbf{q},\mathbf{k})\in\mathbb{R}$输入向量$\mathbf{q}$和$\mathbf{k}$，输出一个实数，一个$\mathbf{q}$与多个$\mathbf{k}$求得的注意力评分通过softmax后得到注意力权重，与$y_i$加权求和便可预测$\hat{y}$。

可以看出，注意力评分其实本质上可以看作一种相似度的度量，$\mathbf{q}$与$\mathbf{k}$越接近则评分越大。

## Additive attention

对于query($x$)和key($x_i$)是不同维度矢量时，可以使用additive attention，通过参数化矩阵分别与$\mathbf{q}$和$\mathbf{k}$相乘变换到相同维度$h$，然后便可求和（理解成做差也可以），最后通过与向量$\mathbf{w}_v$求积得到一个标量作为权重。给定$\mathbf{q}\in\mathbb{R}^q$和$\mathbf{k}\in\mathbb{R}^k$，注意力评分函数为：
$$
a(\mathbf{q}, \mathbf{k}) = \mathbf{w}_v^Ttanh(\mathbf{W}_q\mathbf{q}+\mathbf{W}_k\mathbf{k})\in\mathbb{R}
$$
其中，参数尺寸为：$\mathbf{w}_v\in\mathbb{R}^{h}, \mathbf{W}_q\in\mathbb{R}^{h\times q}, \mathbf{W}_k\in\mathbb{R}^{h\times k}$，乘起来就是$[1\times n] = [1\times h]\cdot tanh\left([h\times q] \cdot [q\times n] + [h\times k]\cdot[k\times n]\right)$

参数量为$h\times(1+k+q)$。矩阵相乘可以等价于偏置为0的单个Linear层，这也是常见的工程实现方式。

```python
import torch
from torch import nn


class AdditiveAttention(nn.Module):
    def __init__(self, q_size, k_size, h, dropout=0.5, **kwargs):
        super().__init__(**kwargs)
        self.W_q = nn.Linear(q_size, h, bias=False)
        self.W_k = nn.Linear(k_size, h, bias=False)
        self.w_v = nn.Linear(h, 1, bias=False)
        self.dropout = nn.Dropout(dropout)

    def forward(self, query, key, value):
        # query: [batch_size, n_q, q_size]
        # key: [batch_size, n_kv, k_size]
        # value: [batch_size, n_kv, v_size]

        query, key = self.W_q(query), self.W_k(key)
        # query: [batch_size, n_q, h]
        # key: [batch_size, n_kv, h]

        features = torch.tanh(query.unsqueeze(2) + key.unsqueeze(1))
        # features: [batch_size, n_q, n_kv, h] = [batch_size, n_q, 1, h] + [batch_size, 1, n_kv, h]

        scores = self.w_v(features).squeeze(-1)
        # scores: [b, n_q, n_kv]

        self.attention = nn.functional.softmax(scores, dim=-1)  # softmax on each key-value pair
        # attention: [b, n_q, n_kv]

        result = torch.bmm(self.dropout(self.attention), value)
        # result: [batch_size, n_q, v_size]
        return result

```

## Scaled dot-product attention

如果$\mathbf{q}$和$\mathbf{k}$维度同时为$d$，直接使用向量内积即可作为注意力评分函数，我们知道内积本质上就是余弦相似度。为了规范化方差，将内积除以$\sqrt{d}$即可，有：
$$
a(\mathbf{q},\mathbf{k})=\frac{\mathbf{q}^T\mathbf{k}}{\sqrt{d}}
$$
使用矩阵批量计算，则对于 query: $\mathbf{Q}\in\mathbb{R}^{n\times d}$，key: $\mathbf{K}\in\mathbb{R}^{m\times d}$和 value: $\mathbf{V}\in\mathbb{R}^{m\times v}$，注意力为：
$$
softmax\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d}}\right)\mathbf{V}\in\mathbb{R}^{n\times v}
$$
这种注意力机制没有参数，运算过程也很简单，比较快，实现容易。

```python
import torch
from torch import nn


class DotProductAttetnion(nn.Module):
    def __init__(self, dropout=0.5, **kwargs):
        super().__init__(**kwargs)
        self.dropout = nn.Dropout(dropout)

    def forward(self, query, key, value):
        # query: [batch_size, n_q, d]
        # key: [batch_size, n_kv, d]
        # value: [batch_size, n_kv, v_size]
        d = torch.tensor(query.shape[-1])

        scores = torch.bmm(query, key.transpose(-1,-2)) / torch.sqrt(d)
        # scores: [b, n_q, n_kv] = [b, n_q, d] @ [b, d, n_kv]

        self.attention = nn.functional.softmax(scores, dim=-1)  # softmax on each key-value pair
        # attention: [b, n_q, n_kv]

        result = torch.bmm(self.dropout(self.attention), value)
        # result: [batch_size, n_q, v_size]
        return result

```

## 推广

只要能构造出相同形状的注意力评分，要么参数化要么使用相似性度量，就可以构造出一种注意力机制。比方说使用参数化矩阵$\mathbf{W}_{qk}\in\mathbb{R}^{q\times k}$，设计如下注意力评分函数：
$$
a(\mathbf{q}, \mathbf{k})=\frac{\mathbf{q}^TW_{qk}\mathbf{k}}{\sqrt[4]{q\times k}}
$$
就可以用与内积注意力相似的计算方式，在$\mathbf{q}$和$\mathbf{k}$维度不同的情况下计算注意力了。