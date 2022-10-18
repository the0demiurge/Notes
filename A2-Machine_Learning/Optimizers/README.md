# Optimizers

随机梯度下降的梯度方差比较大，这会导致训练较为困难，不论是optimizer的tricks还是RL的tricks，很多都在于如何减小方差。

## SGD

$$
\mathbf{x} \leftarrow \mathbf{x} - \eta \nabla f_i(\mathbf{x})
$$

## Momentum

使用leaky average，其实就是对梯度进行指数平滑，得到的平滑后的梯度更新迭代点：

$$
\begin{split}\begin{aligned}
\mathbf{v}_t &\leftarrow \beta \mathbf{v}_{t-1} + \mathbf{g}_{t, t-1}, \\
\mathbf{x}_t &\leftarrow \mathbf{x}_{t-1} - \eta_t \mathbf{v}_t.
\end{aligned}\end{split}
$$

## AdaGrad

现在加入一个新的需求，希望学习率随着迭代步数以$$\mathcal{O}(t^{-\frac{1}{2}})$$的速度收敛。但现在存在一个问题：数据分布不均衡。因此我们希望常见的特征梯度参数收敛快，不常见的特征梯度参数收敛慢。这里我们使用变量 $$\mathbf{s}_t$$ 记录每一维特征累计的梯度方差，如下所示（下面的操作都是按位置进行的操作pair-wise）：

$$
\begin{split}\begin{aligned}
    \mathbf{g}_t & = \partial_{\mathbf{w}} l(y_t, f(\mathbf{x}_t, \mathbf{w})), \\
    \mathbf{s}_t & = \mathbf{s}_{t-1} + \mathbf{g}_t^2, \\
    \mathbf{w}_t & = \mathbf{w}_{t-1} - \frac{\eta}{\sqrt{\mathbf{s}_t + \epsilon}} \cdot \mathbf{g}_t.
\end{aligned}\end{split}
$$

这里就不考虑动量了，直接记录每一维度的梯度的累计平方，让这个累计平方较大的梯度参数衰减较快。

### RMSProp

在实践中我比较喜欢这个算法，收敛速度常常显著优于其他算法。

这个算法是基于前面算法思想的改进，Adagrad的s通过不断累计会不断上升，导致梯度会逐渐收敛到0，而且噪声越大收敛越快。RMSProp 使用梯度平方的指数平滑，不再向正无穷累积：

$$
\begin{split}\begin{aligned}
    \mathbf{s}_t & \leftarrow \gamma \mathbf{s}_{t-1} + (1 - \gamma) \mathbf{g}_t^2, \\
    \mathbf{x}_t & \leftarrow \mathbf{x}_{t-1} - \frac{\eta}{\sqrt{\mathbf{s}_t + \epsilon}} \odot \mathbf{g}_t.
\end{aligned}\end{split}
$$
## Adadelta

$$
\begin{aligned}
    \mathbf{s}_t & = \rho \mathbf{s}_{t-1} + (1 - \rho) \mathbf{g}_t^2.
\end{aligned}
$$
$$
\begin{split}\begin{aligned}
    \mathbf{g}_t' & = \frac{\sqrt{\Delta\mathbf{x}_{t-1} + \epsilon}}{\sqrt{{\mathbf{s}_t + \epsilon}}} \odot \mathbf{g}_t, \\
\end{aligned}\end{split}
$$
$$
\begin{aligned}
    \Delta \mathbf{x}_t & = \rho \Delta\mathbf{x}_{t-1} + (1 - \rho) {\mathbf{g}_t'}^2,
\end{aligned}
$$
$$
\begin{split}\begin{aligned}
    \mathbf{x}_t  & = \mathbf{x}_{t-1} - \mathbf{g}_t'. \\
\end{aligned}\end{split}
$$
总的来说和前面几个算法差别不大，只是分成两步，进一步进行平滑了，实践中我很少用这个算法，以前对比测试的时候也没感觉到有什么突出的地方。

## Adam

目前最受欢迎的算法，结合了前面各种算法的特点，不过有时会因为方差控制不良导致发散。我在实践中并没有感受到该算法相比RMSProp的优势，反而常常比不过RMSProp。想让这个算法好用还需要进行预热，不如RMSProp方便。

该算法首先对梯度和梯度平方指数平滑，平滑系数通常取$$\beta_1 = 0.9$$与$$\beta_2 = 0.999$$:
$$
\begin{split}\begin{aligned}
    \mathbf{v}_t & \leftarrow \beta_1 \mathbf{v}_{t-1} + (1 - \beta_1) \mathbf{g}_t, \\
    \mathbf{s}_t & \leftarrow \beta_2 \mathbf{s}_{t-1} + (1 - \beta_2) \mathbf{g}_t^2.
\end{aligned}\end{split}
$$

然后还需要估计$$v_0, s_0$$:

$$
\hat{\mathbf{v}}_0 = \frac{\mathbf{v}_0}{1 - \beta_1^0} \text{ and } \hat{\mathbf{s}}_0 = \frac{\mathbf{s}_0}{1 - \beta_2^0}.
$$

然后和RMSProp类似，区别在于这里使用动量而不是梯度进行更新：

$$
\mathbf{g}_t' = \frac{\eta \hat{\mathbf{v}}_t}{\sqrt{\hat{\mathbf{s}}_t} + \epsilon}.
$$
$$
\mathbf{x}_t \leftarrow \mathbf{x}_{t-1} - \mathbf{g}_t'.
$$
因为Adam使用了动量，我在实践中不喜欢动量，常常会导致收敛变慢，因此较少使用Adam。

## 思考

前面这些算法大多是在梯度上做文章，核心做法就是两个：

1. 对不同维度进行个性化缩放，
2. 对梯度（以及梯度平方）指数平滑，减小方差。

我在参数优化的时候还喜欢使用一个trick，就是将梯度的方向和长度分开使用，使用梯度得到更新方向，使用固定值或其他方法给出步长，这样不会因为