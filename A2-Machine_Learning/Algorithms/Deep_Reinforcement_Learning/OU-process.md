# Ornstein–Uhlenbeck process

```python
from random import gauss

class OrnsteinUhlenbeckProcess(object):
    # Ornstein–Uhlenbeck process
    def __init__(self, dt, theta, sigma, nums=1):
        self.x = [0] * nums
        self.dt = dt
        self.theta = theta
        self.sigma = sigma
        self.nums = nums

    def __call__(self):
        dx = [-self.theta * self.x[i] * self.dt + self.sigma * gauss(0, 1) for i in range(self.nums)]
        self.x = [self.x[i] + dx[i] for i in range(self.nums)]
        return self.x

```

