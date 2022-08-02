# Lecture 2

## 系统辨识

### 线性回归

$$
\hat{y}=\mathbf{\theta}^T\mathbf{z}+\epsilon
$$

现在有数据集$$y_1, \ldots, y_N$$, $$z_1, \ldots, z_N$$，

使用平方损失函数
$$
J=\sum(y_i-\hat{y})
$$
用矩阵表示为

$$
J=\lVert \mathbf{y}-Z\mathbf{\theta}\rVert_2
$$

如果Z满秩，导数等于0，解得
$$
\hat{\mathbf{\theta}}=\left(Z^TZ\right)^{-1}Z^T\mathbf{y}
$$

### 一阶线性模型参数辨识

状态转移模型：$$x_{t+1}=ax_t+bu_t+\epsilon$$

线性回归模型：$$z_t=[x_t, u_t]$$；$$y=x_{t+1}$$；$$\mathbf{\theta}=[a,b]$$

收集数据求解即可，其实就是个回归问题，用其他模型也ok

### MRAC: Model Reference Adaptive Control

ppt里面例子推导很有问题，完全看不懂，所以这里参考[这篇博客](https://blog.csdn.net/weixin_42143018/article/details/103952406)或者[PDF](mrac.pdf)的内容进行介绍。

