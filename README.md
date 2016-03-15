#Optical Tweezers
Analysis for Optical Tweezers

##Dependencies
This software depends upon [NumPy](http://numpy.org), [SciPy](http://scipy.org) and [matplotlib](http://matplotlib.org/), and have
only been tested in Python 2.7.

#Contents
[Examples](#examples)<br />
<a name="examples" />
#Examples
##Creating a Configuration Object
```python
from otz import Calibration
settings = r'[...]/example Voltage Settings.tzt'
x_cal = r'[...]/example Voltage X data.tzt'
y_cal = r'[...]/example Voltage Y data.tzt'
stage_freq = 150
cal = Calibration(settings, stage_freq, x_cal, y_cal)
```

##Plotting PSD
```python
cal.plot_psd()
```

##Plotting Calibration Timestream
```python
cal.xplot.show()
```

##Filtering with PSD
```python
fildered_data = c.band_stop(20,65)
# View filtered and overlay unfiltered
c.plot_psd(vdat = filtered_data, plot_orig=True)
```
