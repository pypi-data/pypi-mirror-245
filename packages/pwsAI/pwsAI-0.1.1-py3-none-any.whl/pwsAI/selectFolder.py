#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   selectFolder.py
@Time    :   2023/05/17 12:46:09
@Author  :   nico 
@Version :   1.0
@description:

This simple folder will make prompt the user to selet the folder in order to select
the parent directory that has all the cell folders and save the path to be run by 
the converRMS.py script. --> in GUI this function is linked to a button. 
'''
import os 
from tkinter import Tk
from tkinter.filedialog import askdirectory 

def select_folder(): 
    print('here')
    filepath = askdirectory(title='Select Folder')  
    print(f' GETTING FILES FROM: {filepath}')
    # close the gui that pops up for the folder seleciton
    return filepath 



if __name__ == "__main__":
    # print the files in this folder 
    filepath = select_folder()
    fileList = [ file for file in os.listdir(filepath)]
    print(fileList)




    