#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   convertNuc.py
@Time    :   2023/05/18 02:10:57
@Author  :   nico 
@Version :   1.0
@Description: 

Convert the saved cube of individual ROIs into hdf5 format and assign it to the
corresponding analyis file in each cell folder 

This file is saved here but needs to be run with pwspyyEnv because usess pwspy pacakge
that is not compatible with current version of PWS_AI ! so yeah this needs to be updated

update, can use subprocess to run it with pwspyEnv to avoid werid shit.
'''

# import functions 
import os 
import matplotlib.pyplot as mpl
import matplotlib.pyplot as plt
import numpy as np
import h5py
import tifffile as tif 
import pwspy 
import pwspy.dataTypes as pwsdt
import rasterio 



### FUNCTIONS ###
def importMask(maskArray,cellFolder,roiName,roiNumber):
    """
    This function will generete a mask to be used with a particular 
    acquisiton object. 

    Args:
        maskArray (nd array ): array of mask, must be of type rasterio.bool_
        cellFolder (str): folder where the acquisition is
        roiName (int): integer for roi name ( if number if not can use string name as well)
    """
    roi = pwsdt.Roi.fromMask(maskArray)
    acq = pwsdt.Acquisition(cellFolder)
    acq.saveRoi(f'{roiName}',roiNumber,roi)
    print(f"uploaded {roiName} {roiNumber}")
    return 

def runCvtNuc(fileList):
    # get list of all cells from path input
    print(fileList)
    return


if __name__ =='__main__':
    # hardcoding path rnow because gui saves the 
    genPath = r'''C:\Users\nai5790\OneDrive - Northwestern University\Sunil - PWS Project\PWS Nuclei segmentation AI code\Test\guiTestData'''
    fileList=[]

    for file in os.listdir(genPath):
        if  not len(file) == 7 and file[4] != '9':
            if file == ".DS_Store":
                # removing DS.STORE 
                os.remove(os.path.join(genPath,file))
            else: 
                fileList.append(os.path.join(genPath,file))

    # now with file List --> run code iteratively through each path
    for i in range(len(fileList)):
        cellPath = fileList[i] 
        # set variables to load in cell folders 
        num = i+1
        filename = os.path.join(cellPath,f'reconstructed_nuclie_cube_Cell{num}.tif')
        # push mask to the pwpsy in each folder 
        # read images using tif.imread
        maskCube = tif.imread(filename)
        # iterate through each mask, convert to rasterio boolean, save to specific acquisiton with specific name 
        roiName = f"AUTO"
        for i in range(len(maskCube)):
            roiNumber = i
            mask = maskCube[i,:,:].astype(rasterio.bool_)
            # run importMask with these parameters to save ROI 
            importMask(mask,cellPath,roiName,roiNumber)
        print('DONE')


