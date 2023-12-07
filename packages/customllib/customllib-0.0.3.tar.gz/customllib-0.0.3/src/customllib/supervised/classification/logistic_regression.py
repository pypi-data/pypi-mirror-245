import copy

import numpy as np

np.seterr(divide='ignore')


class LogisticRegression:

    def __init__(self):
        pass

    def _sigmoid(self, x, w, b):
        z = np.dot(x, w) + b
        fx = 1 / (1 + np.exp(-z))
        return fx

    def _cost(self, x, y, w, b, lambda_=None):
        m = x.shape[0]
        fx = self._sigmoid(x, w, b)
        jwb = -1 * np.sum(np.dot(y, np.log(fx)) + np.dot((1 - y), np.log(1 - fx))) / m
        if lambda_:
            jwb += lambda_ * np.sum(np.square(w)) / (2 * m)
        return jwb

    def _gradient_descent(self, x, y, w, b, lambda_=None):
        m = x.shape[0]
        fx = self._sigmoid(x, w, b)
        dw = np.sum(np.dot((fx - y), x)) / m
        if lambda_:
            dw += lambda_ * w / m
        db = np.sum(fx - y) / m
        return dw, db

    def train(self, x, y, w_init, b_init, alpha, iterations, lambda_):
        cost_history = []
        parameters_history = []

        w = copy.deepcopy(w_init)
        b = copy.deepcopy(b_init)

        for i in range(iterations):
            dw, db = self._gradient_descent(x, y, w, b, lambda_)
            w = w - alpha * dw
            b = b - alpha * db

            if i < 100000:
                cost_history.append(self._cost(x, y, w, b, lambda_))
                parameters_history.append([w, b])

        return w, b, cost_history, parameters_history

    def predict(self, x, w, b):
        yhat = [1 if i > 0.5 else 0 for i in self._sigmoid(x, w, b)]
        return yhat
