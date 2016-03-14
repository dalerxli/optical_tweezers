import Calibration
import matplotlib.pyplot as plt
from scipy import signal

class Timestream:
    """
    Calibrated Voltage Timestream
    """
    def __init__(self, Calibration, voltage):
        self.cal = Calibration
        self.frequencies = []
        self.voltx = []
        self.volty = []
    def band_stop(self, freq_low, freq_high):
        pass
    def plot(self, **kwargs):
        plt.plot(self.frequencies, self.voltx, **kwargs)
        plt.plot(self.frequencies, self.volty, **kwargs)
        plt.show()
    def plotx(self, **kwargs):
        plt.plot(self.frequencies, self.voltx, **kwargs)
        plt.show()
    def ploty(self, **kwargs):
        plt.plot(self.frequencies, self.volty, **kwargs)
        plt.show()


class CalibrationTimestream(Timestream):
    """
    Timestream for free beam.
    """
    pass

class CapturedTimestream(Timestream):
    """
    Timestream for particles captured in beam.
    """
    pass
