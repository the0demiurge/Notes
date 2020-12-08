# 强化学习调优

## 经验

- 先把学习率调到很小试试，比如1e-4；weight decay调到学习率的1/10
- 如果经过了预训练，就减小探索率，从0.5衰减到0.05
- buffer length太长会加重off-policy的不收敛问题，但至少能把延迟的reward包含进来
- 在衰减得不太厉害（要看reward能够延迟多少步得到）的前提下，$$\gamma$$小收敛会更容易
- 网路复杂度从小渐渐变大；sigmoid比relu稳定得多；rrelu比relu稳定且比sigmoid快
- 先调critic再调actor
- reward正则化会表现好一些。网上说让reward10分位处于0点时收敛最稳定。有时在batch内去掉均值和/或方差能变稳定（因为没做reward clipping，这样可以减少极端情况）。网上说不能对reward归一化，但可以通过乘系数改变大小（而且很有用）。梯度的方差在1左右比较好，此时对于每轮100～1000步的环境，让target reward在100～1000分会比较好。
- 网上说[BN会失效](https://zhuanlan.zhihu.com/p/210761985)，因为强化学习的数据分布不断变化，BN会不稳定
- embedding后加入dropout也许会变好
- 多进程获取数据时以获取的数据数量为基准规范训练次数，获取数据的同时进行训练。
- 训练时间量变产生质变，通常要1e6steps以上
- 先跑一轮实验标定一下均值和方差，然后归一化
- batch size不能太小

**致命三要素(Reinforcement Learning, 2nd Edition, Sutton)**：同时满足则一定有不收敛和发散的风险

- 函数逼近
- 自举法：使用当前目标估计值（TD/DP）而不是只依赖于真实收益和完整回报（MC）
- 离轨策略训练（off-policy）

## TRICKS

- GAE
- Prioritized Experience Replay
- Dueling Network
- 一致化特征的level

## 思考

强化学习中常常能见到不平衡样本，大部分情况都是负reward，极少数情况能得到正reward。当replay buffer 中存到的数据大部分都是差不多的sample时，如何能提升强化学习的学习效果，

强化学习常常遇到的问题：

1. 不平衡，稀疏reward，通常大部分动作都是负reward，少部分正reward
2. reward和动作之间的关联性。影响reward的因素有很多，动作只是其中之一
3. $$\epsilon$$-greedy搜索空间过大，随机到的大部分动作其实没什么意义
4. 关键动作：只有少数关键动作对整个环境产生重要影响，改变整个人生的通常是少数选择
5. 遗忘
6. 迁移

### 基于数据的思考

**样本数据不平衡**

[不平衡样本解决方法：4-Machine_Learning/Problems/Imbalance](../../Problems/Imbalance.md)

### 基于仿生学的思考

1. 好吃的和没吃过的优先选择没吃过的

### 探索方式

训练时使用softmax作为概率分布，替代$$\epsilon$$-greedy或者A3C的概率采样，或者DDPG的确定性策略；评估时既可用确定性策略，也可用概率分布采样。

## 数据集

网上看到的别人调参结果，可以作为baseline参考

### [BipedalWalker-v2 PPO](https://zhuanlan.zhihu.com/p/322058020)

| param           | value | Notation                                         |
| --------------- | ----- | ------------------------------------------------ |
| learning rate   | 1e-4  | 学习率                                           |
| Update_timestep | 4000  | 多少次timestep后更新一次                         |
| Action_std      | 0.4   | 动作概率分布的标准差，越大越鼓励explore          |
| K_epochs        | 120   | 对sample的batch进行K次梯度下降更新，多次利用数据 |
| steps           | 1.2e6 | 训练总steps                                      |
| Return          | 300   | 最终结果                                         |

Lyap Reward Shaping

$$\hat{R_t}=R_t+\lambda(R_t-R_{t-1})$$

$$\lambda=0.7$$

使用Lyrp，收敛速度有了约30%提升



