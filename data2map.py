'''
 # @ Author: Enrico Martello
 # @ Create Time: 2021.06.14 22:15
 # @ Modified time: 2022.01.10 11:46
 # @ Description: launcher of the whole software. Opens the first window, and gets the paths.
 '''

import PySimpleGUI as sg
import os.path
import runner
global dataname, imgname


# First the window layout in 2 columns

img_list_column = [
    [sg.Text("Seleziona il file contenente la piantina:\n")],
    [sg.Listbox(values=[], enable_events=True,
                size=(40, 20), key="-IMG LIST-")]
]

xcl_list_column = [
    [sg.Text("Seleziona il file contenente le misure:\n")],
    [sg.Listbox(values=[], enable_events=True,
                size=(40, 20), key="-DATA LIST-")]
]

# ----- Full layout -----
layout = [
    [
        sg.Text("Seleziona la cartella di lavoro:\n"),
        sg.In(size=(25, 1), enable_events=True, key="-WORKING FOLDER-"),
        sg.FolderBrowse()
    ],
    [
        sg.Column(img_list_column),
        sg.Column(xcl_list_column)
    ],
    [sg.Button("Via!"), sg.Exit()]
]

window = sg.Window("Image Viewer", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-WORKING FOLDER-":
        folder_img = values["-WORKING FOLDER-"]
        folder_data = values["-WORKING FOLDER-"]
        try:
            # Get list of files in folder
            img_list = os.listdir(folder_img)
            data_list = os.listdir(folder_img)
            imgnames = [
                f for f in img_list if os.path.isfile(os.path.join(folder_img, f)) and f.lower().endswith((".png", ".gif"))
            ]
            window["-IMG LIST-"].update(imgnames)
            datanames = [
                f for f in data_list if os.path.isfile(os.path.join(folder_data, f)) and f.lower().endswith((".xcl", ".xlsx"))
            ]
            window["-DATA LIST-"].update(datanames)

        except:
            print("*** Error while reading the working folder. ***")
            img_list = []
            data_list = []

    elif event == "-IMG LIST-":  # A file was chosen from the listbox
        try:
            imgname = os.path.join(
                values["-WORKING FOLDER-"], values["-IMG LIST-"][0])
        except:
            pass

    elif event == "-DATA LIST-":  # A file was chosen from the listbox
        try:
            dataname = os.path.join(
                values["-WORKING FOLDER-"], values["-DATA LIST-"][0])
        except:
            pass

    elif event == "Via!":
        # print("Floor map in: {}\nData in: {}".format(imgname,dataname))
        runner.main(imgname, dataname)

        break
window.close()
