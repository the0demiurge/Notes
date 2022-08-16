# [Word2Vec](http://zh.d2l.ai/chapter_natural-language-processing-pretraining/word2vec.html)

原因：

1. one-hot的余弦相似度没有意义
2. 降维

原理：

- 挖掘预料中词汇出现顺序之间的关联，需要注意的是

类别：

- Continuous Bag of Words: 上下文 -> 自己
- Skip-Gram: 自己 -> 上下文（其实也等价于自己->整个句子，毕竟P(x|x)=1）

Skip-Gram推导比较简单，据说性能也比CBOW好，此处就略过CBOW。

## 算法细节

首先定义词向量相似度为余弦相似度，假设词向量的模相同（起码随机初始化的情况下，模的范围差别不会太大），所以可以等价与算向量内积$\mathbf{u}_o^T\mathbf{v}_c$

所以，就可以定义矩阵$W$，其中one-hot编码的词向量$w^T  W= \mathbf{v}$

然后定义词汇之间的条件概率，给定$w_c$的条件下$w_o$发生的概率（其实就是先算余弦相似度然后连上softmax）：

$$
P(w_o|w_c) = \frac{e^{\mathbf{u}_o^T\mathbf{v}_c}}{\sum\limits_ie^{\mathbf{u}_i^T\mathbf{v}_c}}
$$

接下来，假设上下文的词汇相对于当前词汇条件独立：

$$
P(w_{o1},w_{o2}, \ldots |w_c) = P(w_{o1}|w_c)P(w_{o2}|w_c) \ldots
$$

那么对语料库滑窗获取数据集，并最大化Skip-Gram概率：

$$
\prod \limits_{t} \prod \limits _{-m\leq j \leq m}P(w^{t+j}|w^t)
$$

这里我没说$j\neq0$，因为当j=0时P=1，写不写都讲等价。

用极大似然法最大化这个概率，取对数后加负号，得到：

$$
J=-\sum\limits_t\sum\limits_{-m\leq j \leq m} logP(w^{t+j}|w^t)
$$

$$
\log P(w_o \mid w_c) =\mathbf{u}_o^T \mathbf{v}_c - \log\left(\sum_{i} e^{\mathbf{u}_i^\top \mathbf{v}_c}\right)
$$

此处i是对所有词向量加和，每次算梯度要遍历所有词向量比较贵，所以用负采样（感觉也可以叫欠采样），上面的公式后面那项不是求与所有向量相似度之和，而是求随机n个向量相似度之和，渐进意义上是等价的（其实也不等价，还要乘上n_words/n）
