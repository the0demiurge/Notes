```python
import torch
from torch import nn
from torch.autograd import Variable
from torch.nn import functional as F
from torch import multiprocessing as mp
# Defining the Network


def no_op(x, *args, **kwargs):
    return x


class FeedForwardNet(nn.Module):

    def __init__(self, shape=[20, 100, 5], activation_fn=F.rrelu, initializer=nn.init.kaiming_normal, final_layer_afn=no_op,
                 final_layer_init=no_op, bn=False):
        super(FeedForwardNet, self).__init__()

        self.shape = shape
        self.activation_fn = activation_fn
        self.final_layer_afn = final_layer_afn
        self.bn = torch.nn.BatchNorm1d if bn else no_op
        self.initializer = initializer
        self.final_layer_init = final_layer_init

        for index, size in enumerate(zip(shape[:-1], shape[1:])):
            self.__setattr__("fc_{}".format(index),
                             nn.Linear(size[0], size[1]))
            initializer(self.__getattr__("fc_{}".format(index)).weight)
        final_layer_init(self.__getattr__("fc_{}".format(index)).weight)

    def forward(self, x):
        for i in range(len(self.shape) - 2):
            layer = self.__getattr__("fc_{}".format(i))
            # tensorflow feed_forward implemention is bn before activation
            x = self.bn(x)
            x = self.activation_fn(layer(x))
        x = self.final_layer_afn(self.__getattr__(
            "fc_{}".format(len(self.shape) - 2))(x))
        return x


def main():
    net = FeedForwardNet([20, 100, 5])
    optimizer = torch.optim.RMSprop(net.parameters(), lr=1e-4)
    loss_func = torch.nn.MSELoss()

    inputs, labels = Variable(torch.rand(
        [100, 20])), Variable(torch.rand([100, 5]))

    prediction = net(inputs)
    loss = loss_func(prediction, labels)
    optimizer.zero_grad()
    # print(next(net.parameters()).grad)
    # next(net.parameters())._grad.add_(10000)
    loss.backward()
    # print(next(net.parameters()).grad)
    # prediction = net(inputs)
    # loss = loss_func(prediction, labels)

    # loss.backward()
    # print(next(net.parameters()).grad)
    optimizer.step()  # step could run multiple

    inputs, labels = inputs.cuda(), labels.cuda()
    net1, net2 = FeedForwardNet(), FeedForwardNet()
    net1.cuda()
    net2.cuda()
    opt1, opt2 = [torch.optim.RMSprop(n.parameters()) for n in [net1, net2]]
    opt1.zero_grad(), opt2.zero_grad()
    loss = loss_func(net1(inputs), labels)
    for gp, lp in zip(net2.parameters(), net1.parameters()):
        gp._grad = lp.grad
    opt2.step()


if __name__ == '__main__':
    main()

```

