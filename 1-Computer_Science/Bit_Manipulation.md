1. 去掉最右位：`x & (x - 1)`

2. 只要最右位：`x & ~(x - 1)`

3. 加法：

   - Result: XOR

   - Carry: AND