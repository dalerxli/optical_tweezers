import numpy as np
from scipy.optimize import curve_fit, basinhopping
import matplotlib.pyplot as plt
import scipy.signal as sig
from otz.templates import line, log_psd

plt.ioff()

class Calibration:
    step_to_dist = {
            'x': {'f': 27.78, 'b': 37.04},
            'y': {'f': 35.71, 'b': 25.64}
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
        vdata = self.ts['x']
        xplt.plot(self.tdata, vdata)
        xplt.set_xlabel("Time (s)")
        xplt.set_ylabel("Voltage (V)")
        xplt.set_title("X Sensitivity Calibration")
        xfig.show()
        return xfig

    def yplot(self):
        yfig = plt.figure()
        yplt = yfig.add_subplot(111)
        vdata = self.ts['y']
        yplt.plot(self.tdata, vdata)
        yplt.set_xlabel("Time (s)")
        yplt.set_ylabel("Voltage (V)")
        yplt.set_title("Y Sensitivity Calibration")
        return yfig

    def sensitivity(self, axis, direction, lims=None, vdata=None):
        """
        Calculate sensitivity from voltage data.
        TODO: Automatically compute start and stop.
        Returns: Sensitivity in V/um and uncertainty
        """
        if vdata is None:
            vdata = self.ts[axis]
        stepdist = Calibration.step_to_dist[axis][direction]
        sampledist = stepdist / self.rate * self.step_freq
        if lims is None:
            lims = [np.argmax(vdata), np.argmin(vdata)]
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
                line, np.arange(upper-lower), vdata[lower:upper] )
        sensitivity = params[0]/sampledist
        uncertainty = np.sqrt(cov[0,0])/sampledist

        return (sensitivity, uncertainty)

    def stiffness(self, axis=None, direction='f', method="PSD", vdata=None, skip=None):
        if method=="PSD":
            if vdata is None:
                vdata = self.ts[axis]
            f, psd = self.psd(vdata=vdata, skip=skip)
            params, cov = curve_fit(
                    log_psd, f, np.log10(psd))
            sensitivity = self.sensitivity(axis, direction, vdata=vdata[100:])[0]
            print "Sensitivity: {0}".format(sensitivity)
            return (params, cov)
        else:
            raise NotImplementedError("Method {0} not implemented".format(method))

    def band_stop(self, low_f, high_f, axis='x', order=6):
        f_nyq = self.rate / 2
        band_low = low_f / f_nyq
        band_high = high_f / f_nyq
        b, a = sig.butter(order, [band_low, band_high], btype='bandstop')
        w, h = sig.freqs(b, a)
        vdata = self.ts[axis]
        filtered = sig.lfilter(b,a,vdata)
        return filtered

    def plot_band_stop(self, low_f, high_f, axis='x', order=6, plot_orig=False):
        fig = plt.figure()
        xplt = fig.add_subplot(111)
        vdata = self.ts[axis]
        if plot_orig:
            xplt.plot(self.tdata, vdata)
        filtered = self.band_stop(low_f, high_f, axis, order)
        xplt.plot(self.tdata, filtered)
        xplt.set_xlabel("Time (s)")
        xplt.set_ylabel("Voltage (V)")
        xplt.set_title(
            "Order-{order} Butterworth Bandstop Filter ({low}Hz-{high}Hz)".format(
            order=order,low=low_f,high=high_f))
        return fig
    
    def psd(self, axis=None, vdata=None, low_f=2., skip=None):
        if vdata is None:
            vdata = self.ts[axis]
        f, psd = sig.periodogram(vdata, self.rate)
        if skip is not None:
            skip_low = np.searchsorted(f, skip[0], side='left')
            skip_high = np.searchsorted(f, skip[1], side='right')
            f = np.concatenate((f[:skip_low],f[skip_high:]))
            psd = np.concatenate((psd[:skip_low],psd[skip_high:]))
        cutoff = np.searchsorted(f, low_f, side='left')
        return f[cutoff:], psd[cutoff:]

    def plot_psd(self, axis=None, vdata=None, plot_orig=False, fit=False, skip=None):
        f, psd = self.psd(axis, vdata)
        fig = plt.figure()
        psdplt = fig.add_subplot(111)
        psdplt.loglog(f, psd)
        if plot_orig:
            f_orig, psd = sig.periodogram(self.ts[axis], self.rate)
            psdplt.loglog(f_orig, psd)
        if fit:
            (f_0, alpha), cov = self.stiffness(axis=axis,vdata=vdata,skip=skip)
            logpsd = log_psd(f, f_0, alpha)
            psdplt.loglog(f, 10**logpsd)
        psdplt.set_title("PSD")
        psdplt.set_xlabel("Frequency ($Hz$)")
        psdplt.set_ylabel("PSD ($V^2/Hz$)")
        return fig
