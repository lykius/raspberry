"""
calculators/linreg_calculator.py
Process that calculates linear regression of input data.
"""

import numpy as np
from sklearn.linear_model import LinearRegression

from utility.exceptions import *
from pubsub.message import Message


def linreg_calculator(in_q, out_q, out_topic, buffer_size):
    try:
        X = np.zeros(shape=(buffer_size, 1), dtype=np.double)
        y = np.zeros(shape=(buffer_size, 1), dtype=np.double)
        linregr = LinearRegression()
        for i in range(buffer_size):
            in_msg = in_q.get()
            X[i, 0] = in_msg.timestamp
            y[i, 0] = in_msg.data
        while True:
            X = np.roll(X, -1)
            y = np.roll(y, -1)
            in_msg = in_q.get()
            X[buffer_size - 1, 0] = in_msg.timestamp
            y[buffer_size - 1, 0] = in_msg.data
            linregr.fit(X, y)
            out_msg = Message(out_topic, round(linregr.coef_[0, 0], 2))
            out_q.put(out_msg)
    except:
        handle_process_exception(__name__, out_q)
