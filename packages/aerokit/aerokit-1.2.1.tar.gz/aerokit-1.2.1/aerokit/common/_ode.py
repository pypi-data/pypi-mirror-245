# from Numerical Methods in Engineering With Python

import numpy as np
from math import sqrt


def RK4(F, x, y, xStop, h):
    def run_kut4(F, x, y, h):
        # Computes increment of y from Eqs. (7.10)
        K0 = h * F(x, y)
        K1 = h * F(x + h / 2.0, y + K0 / 2.0)
        K2 = h * F(x + h / 2.0, y + K1 / 2.0)
        K3 = h * F(x + h, y + K2)
        return (K0 + 2.0 * K1 + 2.0 * K2 + K3) / 6.0

    X = []
    Y = []
    X.append(x)
    Y.append(y)
    while x < xStop:
        h = min(h, xStop - x)
        y = y + run_kut4(F, x, y, h)
        # Runge-Kutta Methods
        x = x + h
        X.append(x)
        Y.append(y)
    return np.array(X), np.array(Y)


def _rkf45(F, x, y, h):
    # Runge-Kutta-Fehlberg formulas
    C = [37.0 / 378, 0.0, 250.0 / 621, 125.0 / 594, 0.0, 512.0 / 1771]
    D = [2825.0 / 27648, 0.0, 18575.0 / 48384, 13525.0 / 55296, 277.0 / 14336, 1.0 / 4]
    n = len(y)
    K = np.zeros((6, n), dtype=np.float64)
    K[0] = h * F(x, y)
    K[1] = h * F(x + 1.0 / 5 * h, y + 1.0 / 5 * K[0])
    K[2] = h * F(x + 3.0 / 10 * h, y + 3.0 / 40 * K[0] + 9.0 / 40 * K[1])
    K[3] = h * F(x + 3.0 / 5 * h, y + 3.0 / 10 * K[0] - 9.0 / 10 * K[1] + 6.0 / 5 * K[2])
    K[4] = h * F(x + h, y - 11.0 / 54 * K[0] + 5.0 / 2 * K[1] - 70.0 / 27 * K[2] + 35.0 / 27 * K[3])
    K[5] = h * F(
        x + 7.0 / 8 * h,
        y
        + 1631.0 / 55296 * K[0]
        + 175.0 / 512 * K[1]
        + 575.0 / 13824 * K[2]
        + 44275.0 / 110592 * K[3]
        + 253.0 / 4096 * K[4],
    )
    # Initialize arrays {dy} and {E}
    E = np.zeros((n), dtype=np.float64)
    dy = np.zeros((n), dtype=np.float64)
    # Compute solution increment {dy} and per-step error {E}
    for i in range(6):
        dy = dy + C[i] * K[i]
        E = E + (C[i] - D[i]) * K[i]
    # Compute RMS error e
    e = np.sqrt(np.sum(E ** 2) / n)
    return dy, e


def RKF45(F, x, y, xStop, h, tol=1.0e-6):

    X = []
    Y = []
    X.append(x)
    Y.append(y)
    stopper = 0  # Integration stopper(0 = off, 1 = on)
    for i in range(10000):
        dy, e = _rkf45(F, x, y, h)
        # Accept integration step if error e is within tolerance
        if e <= tol:
            y = y + dy
            x = x + h
            X.append(x)
            Y.append(y)
            # Stop if end of integration range is reached
            if stopper == 1:
                break
        # Compute next step size from Eq. (7.24)
        if e != 0.0:
            hNext = 0.9 * h * (tol / e) ** 0.2
        else:
            hNext = h
        # Check if next step is the last one; is so, adjust h
        if (h > 0.0) == ((x + hNext) >= xStop):
            hNext = xStop - x
            stopper = 1
        h = hNext
    return np.array(X), np.array(Y)
