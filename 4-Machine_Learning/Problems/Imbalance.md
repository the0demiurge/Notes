# 不平衡样本

## 采样

1. 过采样（插值）
2. 欠采样（平衡采样/分层采样）：集成学习或batch平衡化

## 权重

- 基于样本比例分配样本权重
- OHEM(Online Hard Example Miniing)：基于loss判断hard example，按照3:1比例选择hard example，忽略其他的easy example。数据集大时提升明显
- Focal Loss：按照loss平滑调整权重

## 异常检测

适用范围：

1. 无标签
2. 有标签但正样本极少

优先使用有监督方法，无监督方法可用于抽取特征后接入到有监督

- 统计模型（假设检验得到异常值，但需要做出假设）
- 线性模型（PCA投射后重建误差）
- 相似度（密度、距离、夹角、超平面划分次数）KNN距离，密度分析(LOF, LOCI, loOP)，超平面划分(Isolation Forest孤立一个样本的最少划分数)，样本夹角方差(ABOD)
- 异常检测+模型融合，使用bagging提升鲁棒性
- 基于业务的特定领域检测

## 人工

小样本的分类边界手工生成数据

## 衡量指标

- ROC
- mAP(全类平均正确率, mean Average Precision)：各类别PR曲线下面积之平均
- prn(precision@Rank n)：假设有n个异常值时的精确度