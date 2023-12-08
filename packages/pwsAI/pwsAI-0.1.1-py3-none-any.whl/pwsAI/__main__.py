'''' 
Author: Nicolas Acosta 
Date: 03.20.22

This file will run a GUI that can be used for fluorescent imaging 
naming. The GUI will allow you to input the following parameters 
for cell naming in the following order:

    - Imaging modality
        - if all then it generates 3 copies of the name (BF,GF,RF)
    - Cell Name 
    - tag/treatment(if applicable)
    - gRNA (if applicable)
    - Halo Tag Protein 
    - Halo Tag Protein concentration 
    - Cell #
 
This script imports the naming function that in naming.py
'''
import PySimpleGUI as sg
from pwsAI.selectFolder import select_folder
from pwsAI.convertRMS import convertrms
from pwsAI.autoSegCube import autoSeg
import numpy as np
from matplotlib import pyplot as plt


######################################################
#################### GUI CODE ########################
######################################################

def main():
    # Define right pannel layout -- each input should have separate key
    topPanel = [
        sg.Frame(title="INSTRUCTIONS",
                 layout=[[sg.Text(
                     "Please use the builtin search function to select the folder with your\ndata. Selection is similar to that done in PWSPY analysis software so please\nselect the parent folder where you have all cell folders!")]
                     , [sg.Push()], [sg.Button("Further Instructions!", key='-finst-')]],
                 size=(595, 120))
    ]

    leftPanel_layout = [[sg.Button('Select Parent Folder!', key='-sf-')]]

    rightPanel_layout = [
        [sg.Frame(title='Output', size=(400, 320), layout=[
            [sg.Text("File Path Below, Check before converting the data\nto RMS to input into the AI")],
            [sg.HSeparator()], [sg.Text("", key='-fpath-')],
            [sg.Button('Get RMS Images', key='-cv_rms-')], [sg.Text("STATUS:\n", key='-rmsGen-')],
            [sg.Text("Threshold Value"), sg.InputText(key='thresh')],
            [sg.Button('Generate Auto ROIs', key='-auto-')], [sg.Text("STATUS:\n", key='-autotxt-')],
            [sg.Button('Push ROI to PWSPY', key='-push-')], [sg.Text("STATUS:\n", key='-pushtext-')]
        ]
                  )]
    ]

    finLayout = [
        [topPanel,
         [sg.HSeparator()],
         [sg.Column(layout=leftPanel_layout), sg.VSeparator(), sg.Column(layout=rightPanel_layout)]]
    ]

    # layout for pop up for further instructions
    popLayout = [[sg.Text(
        'DESCRIPTION:\nThe following AI GUI will generate ROIS for your PROCESSED data.\nThis means that you must have already run the analysis on your dataset in the\nPWSPY analysis software. Once this has been done you can  use this gui to\ngenerate your ROIs. Once it has finished running you will have the ROIs accessible\nin the PWSPY software'),
                  sg.Push(), sg.VSeparator(), sg.Text(
            'STEPS:\n1) Find Cell Folder with all cells with analysis files generated already\n2)Convert the analysis files to RMS to be input into the model.\n3)RUN AI to generate TIF cubes with each slice being a generated\nmask for the nucleus in image \n4)Convert generated ROIs into HDF5 format to be worked with in Analysis Software')]]

    # crate popup window

    popwindow = sg.Window('Further Instructions', layout=popLayout, element_padding=2)

    # Create main  window #
    window = sg.Window('PWS_AI_Gui', layout=finLayout, element_padding=2)

    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Quit':

            break

        # pop up events
        elif event == '-finst-':
            while True:
                popEvent, popValues = popwindow.read()
                if popEvent == sg.WINDOW_CLOSED or popEvent == '-close-':
                    break
                elif popEvent == '-close-':
                    break
        # main window events
        elif event == '-sf-':
            fpath = select_folder()
            # only print the last two entries of the selected folder path
            tpath = fpath.split('/')
            displayPath = tpath[-3] + '/' + tpath[-2] + '/' + tpath[-1]
            window['-fpath-'].update(f'PATH SELECTED\n{displayPath}')
            print('Select Folder Function')
        # conver the iamge to rms
        elif event == '-cv_rms-':
            print('Convert RMS Function')
            fileList = convertrms(fpath)
            window['-rmsGen-'].update('STATUS:\nRMS images generated!')
        # auto roi run in each cell folder, save cube

        elif event == '-auto-':
            # run the code wihtin each file path in fileList, however only plot if its in
            # cell num1 because dont want to be annoying

            allFileData = []
            print(f'FILES LIST {fileList}')

            # file list split and then sort split to see what that looks like
            cellNumList = [int(fp.split('\\')[-1][4:]) for fp in fileList]

            for f in range(len(fileList)):
                # print(f'iterator:{f}\n')
                #  print(f'filename: {fileList[f]}\n')
                t = np.float32(values['thresh'])
                fp = fileList[f]
                # set the num
                num = cellNumList[f]
                # print(f'NUM: {num}')
                # annoyingly i cant figure out how to plot images all at once, so I will save
                # save each array and iteratively plot them after each file
                # return to this later to do this more elegantly and understand logic flow for
                # button press
                data, titles = autoSeg(fp, num, t)
                allFileData.append(data)

            # plot
            if False:
                for data in allFileData:
                    fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(16, 8))
                    for i, ax in enumerate(axs.flatten()):
                        if i < 2:
                            ax.imshow(data[i], cmap='gray')
                            ax.set_title(titles[i])
                        else:
                            ax.imshow(data[i])
                            ax.set_title(titles[i])
                    plt.show()

            window['-autotxt-'].update('STATUS:\nROIs generated!')

        # gets tricky because of different environment
        elif event == '-push-':
            print('Push to PWSPY')
            convertNuc.runCvtNuc(fileList)
            window['-pushtext-'].update('STATUS:\nROIs now in PWSPY!')

        print('Values', values)

    # Finish up by removing from the screen
    window.close()


if __name__ == '__main__':
    main()
