from otz import Calibration
from otz.templates import log_psd
import matplotlib.pyplot as plt
import os

home = os.environ['HOME']
datadir = home + r'/data/'
xcaldata = datadir + r'cal/100_X Voltage Data.txt'
ycaldata = datadir + r'cal/100_Y Voltage Data.txt'
settings = datadir + r'cal/100_Y Voltage Settings.txt'

cal = Calibration(settings, 150, xcaldata, ycaldata)

