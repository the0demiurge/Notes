# 强化学习

## 适合解决什么问题

1. 固定场景：状态空间不大，整个trajectory不长
2. 问题不复杂：没有太多层次化的任务目标，reward好设计
3. 试错成本低：咋作都没事
4. 数据收集容易：百万千万级别的数据量，如果不能把数据收集做到小时级别，整个任务的时间成本就不能与传统的监督学习相比
5. 目标单纯：容易被reward function量化，比如各种super-human的游戏。对于一些复杂的目标，比如几大公司都在强调拟人化，目前没有靠谱的解决方案

## 强化学习的问题

1. 灾难性遗忘：同时数据分布在训练过程中会发生显著变化
2. credit assign：动作空间不能太大
3. reward强依赖：必须容易设计reward function
4. 对抗噪声干扰能力不足：obs有噪声，reward更有噪声，直接导致训练无法收敛
5. mdp假设过强，对于pomdp问题效果大打折扣

## 强化学习训练指标

- 采样动作分布
- Entropy
- Q-function Loss
- Q-function vs Return
- Q1-Q2
- Reward vs Return