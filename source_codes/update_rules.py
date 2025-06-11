#Update rules for tree parity machine

import numpy as np
import random

def theta(t1, t2):
	return 1 if t1 == t2 else 0

def hebbian(W, X, sigma, tau1, tau2, l):
	k, n = W.shape
	for (i, j), _ in np.ndenumerate(W):
		W[i, j] += X[i, j] * tau1 * theta(sigma[i], tau1) * theta(tau1, tau2)
		W[i, j] = np.clip(W[i, j] , -l, l)

def anti_hebbian(W, X, sigma, tau1, tau2, l):
	k, n = W.shape
	for (i, j), _ in np.ndenumerate(W):
		W[i, j] -= X[i, j] * tau1 * theta(sigma[i], tau1) * theta(tau1, tau2)
		W[i, j] = np.clip(W[i, j], -l, l)

def random_walk(W, X, sigma, tau1, tau2, l):
	k, n = W.shape
	for (i, j), _ in np.ndenumerate(W):
		W[i, j] += X[i, j] * theta(sigma[i], tau1) * theta(tau1, tau2)
		W[i, j] = np.clip(W[i, j] , -l, l)

def dynamic_row(W, X, sigma, tau1, tau2, l):
    k, n = W.shape
    for i in range(k):
        input_vector = X[i]
        num_ones = np.sum(input_vector == 1)
        rule = 'hebbian' if num_ones > len(input_vector) // 2 else 'randomwalk'

        for j in range(n):
            if rule == 'hebbian':
                W[i, j] += X[i, j] * tau1 * theta(sigma[i], tau1) * theta(tau1, tau2)
            else:  # random_walk
                W[i, j] += X[i, j] * theta(sigma[i], tau1) * theta(tau1, tau2)

            W[i, j] = np.clip(W[i, j], -l, l)

def dynamic_matrix(W, X, sigma, tau1, tau2, l):
    num_ones = np.sum(W == 1)
    total_elements = W.size
    rule = 'hebbian' if num_ones > total_elements // 2 else 'randomwalk'

    k, n = W.shape
    for (i, j), _ in np.ndenumerate(W):
        if rule == 'hebbian':
            W[i, j] += X[i, j] * tau1 * theta(sigma[i], tau1) * theta(tau1, tau2)
        else:  # random_walk
            W[i, j] += X[i, j] * theta(sigma[i], tau1) * theta(tau1, tau2)

        W[i, j] = np.clip(W[i, j], -l, l)

def random_eve(W, X, sigma, tau1, tau2, l):
    random.choice([hebbian, random_walk])(W, X, sigma, tau1, tau2, l)
