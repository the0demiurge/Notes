import numpy as np


class MultiArmedBandit(object):
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def rollout(self, i=None):
        if i is None:
            return np.random.normal(self.mu, self.sigma)
        else:
            return np.random.normal(self.mu[i], self.sigma[i])
