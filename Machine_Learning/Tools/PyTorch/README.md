# 流程

定义网络

```python
class Net(nn.Module):
    def forward(self, x):
        y = f(x, ...)
        return y
```

训练

```python
for ...:
    inputs, labels = Tensor(IN), Tensor(OUT)
    optimizer.zero_grad()
    outputs = net(inputs)
    loss = loss_function(outputs, labels)
    loss.backward()
    optimizer.step()
```

# 使用 GPU

```python
device = torch.device('cuda:1') if torch.cuda.is_available() else 'cpu'
input_data = data.to(device)
model = MyModel(...).to(device)
```

所有的 Tensor 都有一个 to(device) 方法

# 不反向传播

```python
with torch.no_grad():
    ...
```

# 保存/载入数据

```python
torch.save(net, 'net.pkl')
net = torch.load('net.pkl')
```

```python
torch.save(net.state_dict(), 'net_parm.pkl')
net = Net()
net.load_state_dict(torch.load('net_parm.pkl'))
```

# 异步梯度累积

梯度累积

```python
optimizer.zero_grad()  # 先把梯度清零
loss = loss_function(...)
loss.backward()
```

梯度传递

```python
with mutex_lock():
    global_net._grad = local_net.grad
    global_optimizer.step()
```

