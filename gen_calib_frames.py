import glob
import astropy.io.fits as fits
import astropy.visualization
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os.path
from visualize import visualize_image

#reads FITS image and returns tuple (array, exptime)
def read_data(filepath):
    hdul = fits.open(filepath)
    array =  hdul[0].data
    exptime = hdul[0].header["EXPTIME"]
    hdul.close()
    print("Done reading ", filepath, ": exptime = ", exptime)
    return(array, exptime)

#path to directory with data
raw_data_dir = 'observation_data'
bias_dir = os.path.join(raw_data_dir,'BIAS')

inputpattern = os.path.join (bias_dir,'*.FIT')
inputfilepaths = sorted(glob.glob(inputpattern))#makes list of all input paths for bias frames & sorts it

"""MasterBias"""
#read data from all bias images, gen data cube, find mean to make masterbias
datalist=[]
for path in inputfilepaths:
    (data,exptime) = read_data(inputfilepath)
    datalist.append(data)
cube = np.dstack(datalist)
masterbias = np.float32(np.mean(cube,axis=2))
np.save(masterbias.npy, masterbias)
visualize_image(masterbias,scale='zscale')
plt.savefig('masterbias.png')
print('Masterbias generated')

"""MasterDark"""


