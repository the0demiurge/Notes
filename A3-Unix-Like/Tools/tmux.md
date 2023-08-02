# Tmux

- new session: `tmux new-session -d -s <session-name>`
- kill session: `tmux kill-session -t <session-name>`
- split window: `tmux split-window -h -t <session-name>:<window-number>`
- select pane: `tmux select-pane -t <session-name>:<window-number>.<pane-number>`
- run command: `tmux send-keys -t <session-name>:<window-number>.<pane-number>`

```bash
#!/bin/bash
set -e
echo '尝试结束之前的任务'
tmux kill-session -t fusion||true
echo '创建tmux session'
tmux new-session -d -s fusion

echo '创建window'
tmux split-window -h -t fusion:0
tmux split-window -v -t fusion:0
tmux select-pane -t fusion:0.0
tmux split-window -v -t fusion:0
tmux split-window -h -t fusion:0

echo '等待bash 10s'
sleep 10

echo '启动任务'
tmux send-keys -t fusion:0.0 './ws/0sensev2x/run/1.sh' C-m
tmux send-keys -t fusion:0.1 './ws/0sensev2x/run/2.sh' C-m
tmux send-keys -t fusion:0.2 './ws/0sensev2x/run/3.sh' C-m
tmux send-keys -t fusion:0.3 'echo HMI暂时不支持，跳过' C-m
#tmux send-keys -t fusion:0.3 './ws/0sensev2x/run/4.sh' C-m
tmux send-keys -t fusion:0.4 './ws/0sensev2x/run/5.sh' C-m

sleep 3
tmux attach-session -t fusion
```
