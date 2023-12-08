#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   convertRMS.py
@Time    :   2023/05/17 15:58:40
@Author  :   nico 
@Version :   1.0
@Description: 

This function will iterate through the file path that was found in selectFolder.py
and extract the RMS files from the analysis cubes. It will then save it in the cell 
folder under, rms.tif
'''
import os 
from tkinter import Tk
from tkinter.filedialog import askdirectory 
import h5py
import tifffile as tif
import numpy as np
import cv2 as cv

def convertrms(dataPath):
    # generate the paths for each of the cell folders, save it in a list 
    fileList = [] 
    for file in os.listdir(dataPath):
        if file.startswith('C'):
            if  not len(file) == 7 and file[4] != '9':
                if file == ".DS_Store":
                    # removing DS.STORE 
                    os.remove(os.path.join(dataPath,file))
                else: 
                    fileList.append(os.path.join(dataPath,file))
                # set cell path 
                cellPath = os.path.join(dataPath,file)
                # once you have cell path, open up the analyiss folder and get the rms 
                fullFileName = os.path.join(cellPath,'PWS/analyses/analysisResults_AD.h5')
                f = h5py.File(fullFileName,'r')
                rmsArray = f['rms']
                #print(np.min(rmsArray),np.max(rmsArray))
                # normalize cv to 0-255 and save it as 8 bit to input intp the model!
                rmsArrayNorm = cv.normalize(np.array(rmsArray),None,0,255,cv.NORM_MINMAX).astype(np.uint8)
                tif.imsave(os.path.join(cellPath,f'rms_{file}.tif'),rmsArrayNorm) 

    return fileList


if __name__ == '__main__':
    # load given path name
    filepath = askdirectory()
    convertrms(filepath)

