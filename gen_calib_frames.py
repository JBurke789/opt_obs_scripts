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
dark_dir = os.path.join(raw_data_dir,"DARK")
Rflat_dir= os.path.join(raw_data_dir,'FLAT/R')
Bflat_dir= os.path.join(raw_data_dir,'FLAT/B')

bias_inputpattern = os.path.join (bias_dir,'*.FIT')
bias_inputfilepaths = sorted(glob.glob(bias_inputpattern))#makes list of all input paths for bias frames & sorts it
dark_inputpattern = os.path.join (dark_dir,'*.FIT')
dark_inputfilepaths = sorted(glob.glob(dark_inputpattern))
Rflat_inputpattern = os.path.join(Rflat_dir,'*.FIT')
Rflat_inputfilepaths = sorted(glob.glob(Rflat_inputpattern))
Bflat_inputpattern = os.path.join(Bflat_dir,'*.FIT')
Bflat_inputfilepaths = sorted(glob.glob(Bflat_inputpattern))

"""MasterBias"""
#read data from all bias images, gen data cube, find mean to make masterbias
bias_datalist=[]
for path in bias_inputfilepaths:
    (data,exptime) = read_data(inputfilepath)
    bias_datalist.append(data)
bias_cube = np.dstack(bias_datalist)
masterbias = np.float32(np.mean(bias_cube,axis=2))
np.save(masterbias.npy, masterbias)
visualize_image(masterbias,scale='zscale')
plt.savefig('masterbias.png')
print('Masterbias generated')

"""MasterDark"""
dark_datalist = []
for i in dark_inputfilepaths:
    (data,exptime) = read_data(i)
    normed_data_mb = (data - masterbias)/exptime
    dark_datalist.append(normed_data_mb)
dark_cube = np.dstack(datalist)
masterdark = np.float32(np.median(dark_cube,axis=2))
np.save(masterdark.npy, masterdark)
visualize_image(masterdark,scale='zscale')
plt.savefig('masterdark.png')
print('Masterdark generated')

"""MasterFlat"""
#R filter
Rflat_datalist = []
for i in Rflat_inputfilepaths:
    (data,exptime) = read_data(i)#extract flats
    data_mb_md = data - masterbias - masterdark/exptime#subtract mb and rescaled md
    norm_data_mb_md = data_mb_md/np.median(data_mb_md)#normalise flats
    Rflat_datalist.append(norm_data_mb_md)
Rflat_cube = np.dstack(Rflat_datalist)
masterRflat = np.float32(np.median(Rflat_cube, axis=2))
np.save(masterRflat.npy, masterRflat)
visualize_image(masterRflat,scale='zscale')
plt.savefig('masterRflat.png')
print('R Masterflat generated')
#B filter
Bflat_datalist = []
for i in Bflat_inputfilepaths:
    (data,exptime) = read_data(i)#extract flats
    data_mb_md = data - masterbias - masterdark/exptime#subtract mb and rescaled md
    norm_data_mb_md = data_mb_md/np.median(data_mb_md)#normalise flats
    Bflat_datalist.append(norm_data_mb_md)
Bflat_cube = np.dstack(Bflat_datalist)
masterBflat = np.float32(np.median(Bflat_cube, axis=2))
np.save(masterBflat.npy, masterBflat)
visualize_image(masterBflat,scale='zscale')
plt.savefig('masterBflat.png')
print('B Masterflat generated')

print('All calibration frames generated')