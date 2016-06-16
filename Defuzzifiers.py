import numpy as np


class centroid:

    def __init__(self, input_values, upperbond, lowerbond):
        self.fuzzified_outputMax = upperbond
        self.fuzzified_outputMax = lowerbond
        self.input_values = input_values
        self.len = len(input_values)

    @staticmethod
    def sum(y, theta):
        t1, t2 = 0.0, 0.0
        for i in range(len(y)):
            t1 += (y[i] * theta[i])
            t2 += theta[i]
        if t2 == 0:
            return -1
        return t1 / t2

    def __call__(self, clcr):
        y1, y2 = 0.0, self.len
        theta, delta, h = np.zeros([self.len]), np.zeros([self.len]), np.zeros([self.len])
        for i in range(self.len):
            theta[i] = h[i] = (self.fuzzified_outputMax[i] + self.fuzzified_outputMax[i]) / 2
            delta[i] = (self.fuzzified_outputMax[i] - self.fuzzified_outputMax[i]) / 2
        y1 = self.sum(self.input_values, h)
        cn = 0
        while abs(y2 - y1) > 0.000000001:
            cn += 1
            if cn > 1:
                y1 = y2
            e = 0
            for i in range(self.len):
                if self.input_values[i] <= y1 <= self.input_values[i + 1]:
                    e = i
                    break
            for i in range(e):
                if clcr > 0:
                    theta[i] = h[i] - delta[i]
                else:
                    theta[i] = h[i] + delta[i]
            for i in range(e, self.len):
                if clcr > 0:
                    theta[i] = h[i] + delta[i]
                else:
                    theta[i] = h[i] - delta[i]
            y2 = self.sum(self.input_values, theta)
        return y2
