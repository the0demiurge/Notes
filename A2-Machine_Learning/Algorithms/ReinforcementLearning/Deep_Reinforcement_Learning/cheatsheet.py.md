```python
from typing import Any
import torch
F = torch.nn.functional
rewards = states = next_states = dones = actions = torch.tensor([])


class Self(object):
    def __getattribute__(self, __name: str) -> Any:
        pass


self = Self()


def GAE(gamma, lmbda, td_delta):
    td_delta = td_delta.detach().numpy()
    advantage_list = []
    advantage = 0.0
    for delta in td_delta[::-1]:
        advantage = gamma * lmbda * advantage + delta
        advantage_list.append(advantage)
    advantage_list.reverse()
    return torch.tensor(advantage_list, dtype=torch.float)

# ac
td_target = rewards + self.gamma * self.critic(next_states) * (1 - dones)
td_delta = td_target - self.critic(states)  # 时序差分误差
log_probs = torch.log(self.actor(states).gather(1, actions))

actor_loss = torch.mean(-log_probs * td_delta.detach())
critic_loss = torch.mean(F.mse_loss(self.critic(states), td_target.detach()))


# ppo
td_target = rewards + self.gamma * self.critic(next_states) * (1 - dones)
td_delta = td_target - self.critic(states)
advantage = GAE(self.gamma, self.lmbda, td_delta.cpu()).to(self.device)
old_log_probs = torch.log(self.actor(states).gather(1, actions)).detach()
for i in range(3):
    log_probs = torch.log(self.actor(states).gather(1, actions))
    ratio = torch.exp(log_probs - old_log_probs)
    surr1 = ratio * advantage
    surr2 = torch.clamp(ratio, 1 - self.eps, 1 + self.eps) * advantage  # 截断

    actor_loss = torch.mean(-torch.min(surr1, surr2))  # PPO损失函数
    critic_loss = torch.mean(F.mse_loss(self.critic(states), td_target.detach()))


# dqn
q_values = self.q_net(states).gather(1, actions)  # Q值
# 下个状态的最大Q值
max_next_q_values = self.target_q_net(next_states).max(1)[0].view(-1, 1)
q_targets = rewards + self.gamma * max_next_q_values * (1 - dones)  # TD误差目标

dqn_loss = torch.mean(F.mse_loss(q_values, q_targets))  # 均方误差损失函数


# ddpg
next_q_values = self.target_critic(next_states, self.target_actor(next_states))
q_targets = rewards + self.gamma * next_q_values * (1 - dones)

critic_loss = torch.mean(F.mse_loss(self.critic(states, actions), q_targets))
actor_loss = -torch.mean(self.critic(states, self.actor(states)))


# sac
next_actions, log_prob = self.actor(next_states)  # 这里面 next_actions 是动作的概率密度，梯度能传播到 q_value 并最终传到 actor loss
entropy = -log_prob
q1_value = self.target_critic_1(next_states, next_actions)
q2_value = self.target_critic_2(next_states, next_actions)
next_value = torch.min(q1_value, q2_value) + self.log_alpha.exp() * entropy
td_target = rewards + self.gamma * next_value * (1 - dones)

critic_1_loss = torch.mean(F.mse_loss(self.critic_1(states, actions), td_target.detach()))
critic_2_loss = torch.mean(F.mse_loss(self.critic_2(states, actions), td_target.detach()))
actor_loss = torch.mean(-self.log_alpha.exp() * entropy - torch.min(q1_value, q2_value))
alpha_loss = torch.mean((entropy - self.target_entropy).detach() * self.log_alpha.exp())


# ppo:
# 1. batch size
# 2. model hidden size
# 3. max reuse

```
