# [矩阵微积分](https://zh.m.wikipedia.org/zh-hans/%E7%9F%A9%E9%98%B5%E5%BE%AE%E7%A7%AF%E5%88%86)

分子记法：结果的形状与分子维度相同，与分母相反；分布记法反之。

1. 标量求导
   1. **标量对标量求导**: $$\frac{1 \times 1}{1 \times 1} \rightarrow {1 \times 1}$$
      - $$\frac{dy}{dx}$$
2. 向量求导
   1. **向量对标量求导**: $$\frac{m \times 1}{1 \times 1} \rightarrow {m \times 1}$$
       - $$\frac{\partial\begin{bmatrix} y_1 & y_2 & \ldots & y_m\end{bmatrix}^T}{\partial x}=\begin{bmatrix}\frac{\partial y_1}{\partial x} & \frac{\partial y_2}{\partial x} & \ldots & \frac{\partial y_m}{\partial x}\end{bmatrix}^T$$
   1. **标量对向量求导**（梯度）: $$\frac{1 \times 1}{n \times 1} \rightarrow {1 \times n}$$
       - $${\displaystyle \nabla _{\mathbf {u} }f=\left({\frac {\partial f}{\partial \mathbf {x} }}\right)^{\top }\mathbf {u} }$$
       - $$\frac{\partial y}{\partial \begin{bmatrix} x_1 & x_2 & \ldots & x_n\end{bmatrix}^T} = \begin{bmatrix}\frac{\partial y}{\partial x_1} & \frac{\partial y}{\partial x_2} & \ldots & \frac{\partial y}{\partial x_n}\end{bmatrix}$$
   1. **向量对向量求导**: $$\frac{m \times 1}{n \times 1} \rightarrow {m \times n}$$
       - $${\displaystyle d\,\mathbf {f} (\mathbf {v} )={\frac {\partial \mathbf {f} }{\partial \mathbf {v} }}d\,\mathbf {v} }$$
       - $$\frac{\partial\begin{bmatrix} y_1 & y_2 & \ldots & y_m\end{bmatrix}^T}{\partial \begin{bmatrix} x_1 & x_2 & \ldots & x_n\end{bmatrix}^T}=\begin{bmatrix} \frac{\partial y_1}{\partial x_1} & \frac{\partial y_1}{\partial x_2} & \cdots & \frac{\partial y_1}{\partial x_n}\\ \frac{\partial y_2}{\partial x_1} & \frac{\partial y_2}{\partial x_2} & \cdots & \frac{\partial y_2}{\partial x_n} \\ \vdots & \vdots & \ddots & \vdots \\ \frac{\partial y_m}{\partial x_1} & \frac{\partial y_m}{\partial x_2} & \cdots & \frac{\partial y_m}{\partial x_n} \end{bmatrix}$$
3. 矩阵求导
   1. **矩阵对标量求导**
       - $$\frac {\partial \mathbf {Y} }{\partial x}}={\begin{bmatrix}{\frac {\partial y_{11}}{\partial x}}&{\frac {\partial y_{12}}{\partial x}}&\cdots &{\frac {\partial y_{1n}}{\partial x}}\\{\frac {\partial y_{21}}{\partial x}}&{\frac {\partial y_{22}}{\partial x}}&\cdots &{\frac {\partial y_{2n}}{\partial x}}\\\vdots &\vdots &\ddots &\vdots \\{\frac {\partial y_{m1}}{\partial x}}&{\frac {\partial y_{m2}}{\partial x}}&\cdots &{\frac {\partial y_{mn}}{\partial x}}\\\end{bmatrix}$$
   1. **标量对矩阵求导**
       - $$\nabla _{\mathbf {X} }y(\mathbf {X} )={\frac {\partial y(\mathbf {X} )}{\partial \mathbf {X} }}$$
       - $$\frac {\partial y}{\partial \mathbf {X} }}={\begin{bmatrix}{\frac {\partial y}{\partial x_{11}}}&{\frac {\partial y}{\partial x_{21}}}&\cdots &{\frac {\partial y}{\partial x_{p1}}}\\{\frac {\partial y}{\partial x_{12}}}&{\frac {\partial y}{\partial x_{22}}}&\cdots &{\frac {\partial y}{\partial x_{p2}}}\\\vdots &\vdots &\ddots &\vdots \\{\frac {\partial y}{\partial x_{1q}}}&{\frac {\partial y}{\partial x_{2q}}}&\cdots &{\frac {\partial y}{\partial x_{pq}}}\\\end{bmatrix}$$
       - 标量函数*f*(**X**)关于矩阵**X**在方向**Y**的**方向导数**可写成
       $$\nabla _{\mathbf {Y} }f=\operatorname {tr} \left({\frac {\partial f}{\partial \mathbf {X} }}\mathbf {Y} \right)$$
