import numpy as np
from scipy.optimize import curve_fit, basinhopping
import matplotlib.pyplot as plt
import scipy.signal as sig
from otz.templates import line, log_psd

plt.ioff()

class Calibration:
    step_to_dist = {
            'x': {'f': 35.71, 'b': 25.64},
            'y': {'f': 27.78, 'b': 37.04}
            }
    def __init__(self, settings_file, step_freq, cal_x_volt, cal_y_volt):
        self.settings = self.load_settings(settings_file)
        self.step_freq = step_freq
        self.cal_x_volt = np.loadtxt(cal_x_volt).astype(float)
        self.cal_y_volt = np.loadtxt(cal_y_volt).astype(float)
        self.ts = {
            'x': self.cal_x_volt[:,0],
            'y': self.cal_y_volt[:,1]
            }
        self.rate = self.settings['Sample Rate']

    @property
    def tdata(self):
        return np.arange(len(self.ts['x']))/self.rate

    def load_settings(self, settings):
        setdict = {}
        with open(settings) as s:
            for line in s:
                (key, val) = line.split(':')
                setdict[key] = float(val)
        return setdict

    def xplot(self):
        xfig = plt.figure()
        xplt = xfig.add_subplot(111)
        vdat = self.ts['x']
        xplt.plot(self.tdata, vdat)
        xplt.set_xlabel("Time (s)")
        xplt.set_ylabel("Voltage (V)")
        xplt.set_title("X Sensitivity Calibration")
        xfig.show()
        return xfig

    def yplot(self):
        yfig = plt.figure()
        yplt = yfig.add_subplot(111)
        vdat = self.ts['y']
        yplt.plot(self.tdata, vdat)
        yplt.set_xlabel("Time (s)")
        yplt.set_ylabel("Voltage (V)")
        yplt.set_title("Y Sensitivity Calibration")
        return yfig

    def sensitivity(self, axis, direction, lims=None, vdat=None):
        """
        Calculate sensitivity from voltage data.
        TODO: Automatically compute start and stop.
        Returns: Sensitivity in V/um and uncertainty
        """
        if vdat is None:
            vdat = self.ts[axis]
        stepdist = Calibration.step_to_dist[axis][direction]
        sampledist = stepdist / self.rate * self.step_freq
        if lims is None:
            lims = [np.argmax(vdat), np.argmin(vdat)]
            start = min(lims)
            stop = max(lims)

            center = int((stop-start)/2+start)

            width = int((stop-start)/4)

            lower = center-width
            upper = center+width
        else:
            lower = lims[0]
            upper = lims[1]
        params, cov = curve_fit(
                line, np.arange(upper-lower), vdat[lower:upper] )
        sensitivity = params[0]/sampledist
        uncertainty = np.sqrt(cov[0,0])/sampledist

        return (sensitivity, uncertainty)

    def band_stop(self, low_f, high_f, axis='x', order=6):
        f_nyq = self.rate / 2
        band_low = low_f / f_nyq
        band_high = high_f / f_nyq
        b, a = sig.butter(order, [band_low, band_high], btype='bandstop')
        w, h = sig.freqs(b, a)
        vdat = self.ts[axis]
        filtered = sig.lfilter(b,a,vdat)
        return filtered

    def plot_band_stop(self, low_f, high_f, axis='x', order=6, plot_orig=False):
        fig = plt.figure()
        xplt = fig.add_subplot(111)
        vdat = self.ts[axis]
        if plot_orig:
            xplt.plot(self.tdata, vdat)
        filtered = self.band_stop(low_f, high_f, axis, order)
        xplt.plot(self.tdata, filtered)
        xplt.set_xlabel("Time (s)")
        xplt.set_ylabel("Voltage (V)")
        xplt.set_title(
            "Order-{order} Butterworth Bandstop Filter ({low}Hz-{high}Hz)".format(
            order=order,low=low_f,high=high_f))
        return fig
    
    def psd(self, axis='x', vdat=None):
        if vdat is None:
            vdat = self.ts[axis]
        return sig.periodogram(vdat, self.rate)

    def plot_psd(self, axis='x', vdat=None, plot_orig=False):
        f, psd = self.psd(axis, vdat)
        fig = plt.figure()
        psdplt = fig.add_subplot(111)
        psdplt.loglog(f, psd, basey=np.e)
        if plot_orig:
            f, psd = sig.periodogram(self.ts[axis], self.rate)
            psdplt.loglog(f, psd)
        psdplt.set_title("PSD")
        psdplt.set_xlabel("Frequency ($Hz$)")
        psdplt.set_ylabel("PSD ($V^2/Hz$)")
        return fig
