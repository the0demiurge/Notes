# PaperList

## Reward 设计

有效的：

- [Reward Centering](https://arxiv.org/abs/2405.09999)：工业实践中手动构建Reward时也会注意的要点，Sutton带的团队用了更多自动化方法动态修改Reward分布，提升训练收敛稳定性。

## 结合人工经验与RL

有效的：

- [InstructGPT](https://arxiv.org/abs/2203.02155)：约束RL探索出的新策略与SL的旧策略的距离，减少reward hacking导致的行为异常。
- [Residual Reinforcement Learning for Robot Control](https://arxiv.org/abs/1812.03201)：残差控制，我目前还没实践过，可以通过限制RL探索范围，减少无效探索空间，并且能避免离谱探索。
- [SERL](https://github.com/rail-berkeley/serl)：就是SAC，但是replay buffer混入了人工采集的transition，肯定会有效，就是目前实验使用的case都太简单了。
- [GAIL](https://arxiv.org/abs/1606.03476)：实践上效果非常好，比纯探索成功率显著提升。

不一定有效的：

- 巡迹训练（RL训练时reward加入与采集的轨迹状态之差），当episode时间较长则很容易跟踪丢；如果采集的轨迹存在长时间静止或其他脏数据将显著破坏模型行为

无效的：

- [Imitation is Not Enough](https://arxiv.org/abs/2212.11419)，waymo的研究，同时进行RL+SL训练，实践上效果很差

## 训练方法

- 使用RL训练模型池后用Dagger蒸馏到单个模型，效果特别好，当前使用RL落地的best pratice，可以保证可靠性，避开了RL最大的劣势

## Tricks
- Loss of Plasticity in Deep Continual Learning: 从感知训练RL的时候，需要进行数据增强，不然会出现可塑性下降