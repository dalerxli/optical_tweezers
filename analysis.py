from otz import Calibration
from otz.templates import log_psd
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
import os

home = os.environ['HOME']
datadir = home + r'/data/'
fdata = {
    100: {
        'xcaldata': datadir + r'cal/100_X Voltage Data.txt',
        'ycaldata': datadir + r'cal/100_Y Voltage Data.txt',
        'settings': datadir + r'cal/100_Y Voltage Settings.txt'
        },
    200: {
        'xcaldata': datadir + r'cal/200_X Voltage Data.txt',
        'ycaldata': datadir + r'cal/200_Y Voltage Data.txt',
        'settings': datadir + r'cal/200_Y Voltage Settings.txt'
        },
    300: {
        'xcaldata': datadir + r'cal/300_X Voltage Data.txt',
        'ycaldata': datadir + r'cal/300_Y Voltage Data.txt',
        'settings': datadir + r'cal/300_Y Voltage Settings.txt'
        },
    400: {
        'xcaldata': datadir + r'cal/400_X Voltage Data.txt',
        'ycaldata': datadir + r'cal/400_Y Voltage Data.txt',
        'settings': datadir + r'cal/400_Y Voltage Settings.txt'
        },
    500: {
        'xcaldata': datadir + r'cal/500_X Voltage Data.txt',
        'ycaldata': datadir + r'cal/500_Y Voltage Data.txt',
        'settings': datadir + r'cal/500_Y Voltage Settings.txt'
        },
}

bdata = {
    100: {
        'xcaldata': datadir + r'cal/100_X_back Voltage Data.txt',
        'ycaldata': datadir + r'cal/100_Y_back Voltage Data.txt',
        'settings': datadir + r'cal/100_Y_back Voltage Settings.txt'
        },
    200: {
        'xcaldata': datadir + r'cal/200_X_back Voltage Data.txt',
        'ycaldata': datadir + r'cal/200_Y_back Voltage Data.txt',
        'settings': datadir + r'cal/200_Y_back Voltage Settings.txt'
        },
    300: {
        'xcaldata': datadir + r'cal/300_X_back Voltage Data.txt',
        'ycaldata': datadir + r'cal/300_Y_back Voltage Data.txt',
        'settings': datadir + r'cal/300_Y_back Voltage Settings.txt'
        },
    400: {
        'xcaldata': datadir + r'cal/400_X_back Voltage Data.txt',
        'ycaldata': datadir + r'cal/400_Y_back Voltage Data.txt',
        'settings': datadir + r'cal/400_Y_back Voltage Settings.txt'
        },
    500: {
        'xcaldata': datadir + r'cal/500_X_back Voltage Data.txt',
        'ycaldata': datadir + r'cal/500_Y_back Voltage Data.txt',
        'settings': datadir + r'cal/500_Y_back Voltage Settings.txt'
        },
}

psd = {
    100: datadir + r'psd100rz PSD Data.txt',
    200: datadir + r'psd200rz PSD Data.txt',
    300: datadir + r'psd300rz PSD Data.txt',
    400: datadir + r'psd400rz PSD Data.txt',
    500: datadir + r'psd500rz PSD Data.txt',
}

fcals = OrderedDict(sorted(
    {key: Calibration(data['settings'], 150, data['xcaldata'], data['ycaldata'],psd[key])
            for key, data in fdata.iteritems()}.items()))

bcals = OrderedDict(sorted(
    {key: Calibration(data['settings'], 150, data['xcaldata'], data['ycaldata'],psd[key])
            for key, data in bdata.iteritems()}.items()))

amps=[]
xfsens=[]
yfsens=[]
xferr=[]
yferr=[]
xbsens=[]
ybsens=[]
xberr=[]
yberr=[]

for amp, c in fcals.iteritems():
    amps.append(amp)
    xfsens.append(np.abs(c.sensitivity(axis='x', direction='f', vdata=c.band_stop(25,65)[50:-50])[0]))
    yfsens.append(np.abs(c.sensitivity(axis='y', direction='f', vdata=c.band_stop(25,65,axis='y')[50:-50])[0]))
    xferr.append(c.sensitivity(axis='x', direction='f', vdata=c.band_stop(25,65)[50:-50])[1])
    yferr.append(c.sensitivity(axis='y', direction='f', vdata=c.band_stop(25,65,axis='y')[50:-50])[1])

for amp, c in bcals.iteritems():
    xbsens.append(np.abs(c.sensitivity(axis='x', direction='b', vdata=c.band_stop(25,65)[50:-50])[0]))
    ybsens.append(np.abs(c.sensitivity(axis='y', direction='b', vdata=c.band_stop(25,65,axis='y')[50:-50])[0]))
    xberr.append(c.sensitivity(axis='x', direction='b', vdata=c.band_stop(25,65)[50:-50])[1])
    yberr.append(c.sensitivity(axis='y', direction='b', vdata=c.band_stop(25,65,axis='y')[50:-50])[1])
