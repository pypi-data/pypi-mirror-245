import PySimpleGUI as sg

layout = [
    [sg.Column([sg.Text('Column 1')]), sg.Column([sg.Text('Column 2')])]
]

window = sg.Window('Column Example', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    for column_element in layout[0]:  # Iterate over the first column
        print(column_element)

window.close()
