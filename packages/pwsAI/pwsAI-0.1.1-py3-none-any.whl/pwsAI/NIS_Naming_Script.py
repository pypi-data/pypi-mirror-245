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
## importing packages ##
import PySimpleGUI as sg
from numpy import size

######################################################
#################### GUI CODE ########################
######################################################

# Define right pannel layout -- each input should have separate key 
topPanel = [
        sg.Frame(title ="INSTRUCTIONS",
            layout=[[sg.Text("Please use the builtin search function to select the folder with your \n data. Selection is similar to that done in PWSPY analysis software so please \n select the parent folder where you have all cell folders!. !")]
            ,[sg.Button("Further Instructions!")]],
            size=(595,80))
            ]
            

leftPanel_layout = [
          [sg.Text("Imaging Mode")],
          [sg.Input(size=(30,1),key='-INPUT-')],
          [sg.Text("Cell Name")],
          [sg.Input(size=(30,1),key='-INPUT-')],
          [sg.Text("Tag/Treatment")],
          [sg.Input(size=(30,1),key='-INPUT-')],
          [sg.Text("gRNA")],
          [sg.Input(size=(30,1),key='-INPUT-')],
          [sg.Text("Halo Tag Protein")],
          [sg.Input(size=(30,1),key='-INPUT-')],
          [sg.Text("Concentration")],
          [sg.Input(size=(30,1),key='-INPUT-')],
          [sg.Text("Cell Number")],
          [sg.Input(size=(30,1),key='-INPUT-')],
          [sg.Text("File Type")],
          [sg.Input(size=(30,1),key='-INPUT-')],
          [sg.Button('Generate File Names')]
          ]

rightPanel_layout = [
        [sg.Frame(title='Output',size = (400,320),layout=[
            [sg.Text("Names below. Use first button to increment cell number and the\nsecond to copy to your clipboard:")]
            
            ] 
        )]
        ]


finLayout=[
        [topPanel,
        [sg.HSeparator()],
        [sg.Column(layout=leftPanel_layout),sg.VSeparator(),sg.Column(layout =rightPanel_layout)]]
        ]

# Create window #
window = sg.Window('NIS Naming Tool', layout=finLayout,element_padding=2)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    # Output a message to the window
    window['-OUTPUT1-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")

# Finish up by removing from the screen
window.close()
