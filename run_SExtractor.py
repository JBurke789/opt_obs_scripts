''' runs sextractor for all images'''
import subprocess
import glob
import os.path

'''
define function to run sextractor
'''
def write_sex_cat(imagefilepath,catalogfilepath):
    #print info while running
    print('Running SExtractor:', imagefilepath,'->',catalogfilepath)
    #config files
    paramspath = 'sextractor/params.txt'
    configpath = 'sextractor/default_config.txt'
    convpath= 'sextractor/default_conv.txt'

    #command to run SExtractor
    cmd = ['source-extractor', imagefilepath,
           '-c', configpath,
           '-PARAMETERS_NAME', paramspath,
           '-FILTER_NAME',convpath,
           '-CATALOG_NAME', catalogfilepath,
           '-CATALOG_TYPE', 'FITS_LDAC',
           '-GAIN','2.3',
           '-DETECT_MINAREA', '5.0',
           '-DETECT_THRESH','1.5',
           '-BACK_SIZE', '64',
           '-WEIGHT_TYPE','BACKGROUND',
          ]
    
    res = subprocess.run(cmd, text=True, capture_output=True)

    if (res.returncode !=0):
        print(res.stderr)
        
        
'''
call function in loop
'''
imagedirpath='prered/science_frames/B' #change path to dir with images
imagefilepaths = sorted(glob.glob(os.path.join(imagedirpath,'*.FIT')))

for i in imagefilepaths:
    image_name = os.path.splitext(os.path.basename(i))[0]
    catfilepath = os.path.join(imagedirpath,image_name + '.cat')
    
    write_sex_cat(i,catfilepath)
    