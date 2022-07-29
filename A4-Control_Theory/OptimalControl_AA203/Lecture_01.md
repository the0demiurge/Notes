# Lecture 1

## 状态空间描述

$$
\mathbf{\dot{x}}(t)=\mathbf{f}(\mathbf{x}(t), \mathbf{u}(t), t)
$$

其中：

- a history of control inputs $u_{t}$  during interval $[t_0, t_f]$ is called a *control history*
- a history of state values $x_{t}$  during interval $[t_0, t_f]$ is called a *state* trajectory

## 最优控制例子

### 问题描述

双重积分器：控制一维空间质点位置，控制量为加速度。控制量和状态变量有如下二次积分的关系：
$$
\ddot{s}(t)=a(t)
$$


控制目标：使其状态从$\mathbf{x}_0=[5,0]\rightarrow u_s=[0, 0]$。状态空间表达式（状态转移模型）为：
$$
\begin{bmatrix}
\dot s \\ \dot v
\end{bmatrix}
=
\begin{bmatrix}
0&1\\0&0
\end{bmatrix}
\begin{bmatrix}
s\\v
\end{bmatrix}
+
\begin{bmatrix}
0\\1
\end{bmatrix}
\begin{bmatrix}
a
\end{bmatrix}
$$

### PD 控制器

线性负反馈：
$$
a=-k_p(s-s_{u_s})-k_d(v-v_{u_s})
$$
解微分方程，得到时域响应，即可分析得知当$k_p,k_d>0$时可收敛到设定值。

### 最优控制器

这里的例子中的最优控制比较简单，直接建立最优化模型，开环控制，求解每个时间步的$u$。
$$
min\int_0^{t_f}{\lVert\mathbf{x}(t)\rVert_2^2 +\lVert\mathbf{u}(t)\rVert_2^2}
$$

$$
\begin{array}{rrl}
s.t.&\mathbf{\dot{x}}(t)=&A\mathbf{x}(t)+B\mathbf{u}(t)\\
&\mathbf{\dot{x}}(0)=&\mathbf{x}_0\\
&\mathbf{\dot{x}}(t_f)=&\mathbf{x}_f
\end{array}
$$

- 优化目标：最小化残差和控制量
- 约束条件：
  - 状态转移
  - 边界条件

课程作业代码中：

```
cost = 0
constraints = [x[0]==x_0, x[t_f]=x_f]

for t in [t0 .. tf], do:
	cost = cost + norm(x[t] - x_f)
	x[t+1] == dynamics(x[t], u[t]) -add-to-> constraint

solver.solve()
```
