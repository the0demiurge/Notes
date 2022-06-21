# Q-Learning

Q: 为什么Q-Learning不用重要性采样？

首先，

$$v_\pi(s)=\mathbb E_\pi[G_t|S_t=s]$$

$$q_\pi(s,a)=\mathbb E_\pi[G_t|S_t=s, A_t=a]$$

注意到Q-learning要学习的是$$Q(s,a)=\sum\limits_{s'}P(s'|s,a)\left(R(s')+\gamma \max\limits_{a}Q(s',a)\right)$$

与$$q_\pi(s,a)$$不同，此处$$s'\sim P(s'|s,a)$$，求期望过程中动作$$a$$不是随机变量，而是给定的值，因此不涉及重要性采样。

