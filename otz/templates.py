import numpy as np

def line(x, a, b):
    return a*x+b

def log_psd(f, f_0, alpha):
    return np.log(alpha) - log(f**2 + f_0**2)
