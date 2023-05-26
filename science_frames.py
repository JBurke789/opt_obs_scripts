import glob
import astropy.io.fits as fits
import numpy as np
import os.path
import matplotlib.pyplot as plt
from visualize import visualize_image
'''
applies the calibration frames generated in gen_calib_frames.py to the science frames
'''
#reads FITS image and returns tuple (array, exptime)
def read_data(filepath):
    hdul = fits.open(filepath)
    array =  hdul[0].data
    exptime = hdul[0].header["EXPTIME"]
    hdul.close()
    print("Done reading ", filepath, ": exptime = ", exptime)
    return(array, exptime)
#paths to input and output directories
rawdatadir = 'observation data' # 
Rsciencedir= os.path.join(rawdatadir,'SCIENCE/R')
R_inputpattern = os.path.join(Rsciencedir,'*.FIT')
R_inputfilepaths = sorted(glob.glob(R_inputpattern))
Bsciencedir= os.path.join(rawdatadir,'SCIENCE/B')
B_inputpattern = os.path.join(Bsciencedir,'*.FIT')
B_inputfilepaths = sorted(glob.glob(B_inputpattern))

Routdir = 'R_output_dir'
Boutdir = 'B_output_dir'
#import calibration frames
masterbias  = np.load('masterbias.npy ')
masterdark  = np.load('masterdark.npy ')
masterRflat = np.load('masterRflat.npy')
masterBflat = np.load('masterBflat.npy')


'''R filter'''
for i in R_inputfilepaths:
    #extract and manipulate data
    (data,exptime) = read_data(i)#extract data and exposure time
    data_mb_md = data - masterbias - masterdark*exptime #subtract masterbias and exposure scaled masterdark
    data_mf = data_mb_md/masterRflat # divide by masterflat for R filter
    #visualise and save image
    visualize_image(data_mf,scale='zscale')
    plt.savefig(os.path.join(outdir, os.path.splitext(os.path.basename(i))[0])+'.png',format='png')
    plt.close()
    #save as FIT file
    hdu = fits.PrimaryHDU(data_mf)
    outfilepath =os.path.join(outdir,os.path.basename(i))
    hdu.writeto(outfilepath,overwrite=True)
    
    
'''B filter'''
for i in B_inputfilepaths:
    #extract and manipulate data
    (data,exptime) = read_data(i)#extract data and exposure time
    data_mb_md = data - masterbias - masterdark*exptime #subtract masterbias and exposure scaled masterdark
    data_mf = data_mb_md/masterRflat # divide by masterflat for R filter
    #visualise and save image
    visualize_image(data_mf,scale='zscale')
    plt.savefig(os.path.join(outdir, os.path.splitext(os.path.basename(i))[0])+'.png',format='png')
    plt.close()
    #save as FIT file
    hdu = fits.PrimaryHDU(data_mf)
    outfilepath =os.path.join(outdir,os.path.basename(i))
    hdu.writeto(outfilepath,overwrite=True)