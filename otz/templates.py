import numpy as np

def line(x, a, b):
    return a*x+b

def log_psd(f, f_0, alpha):
    return np.log10(alpha) - np.log10(f**2 + f_0**2)

def quadratic(x, k, y_0):
    return k*x**2 + y_0

def exp_psd(f, f_0, alpha):
    return alpha/(f**2+f_0**2)
