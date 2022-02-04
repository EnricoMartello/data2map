'''
 # @ Author: Enrico Martello
 # @ Create Time: 2022.01.10 11:34
 # @ Modified time: 2022.01.10 11:47
 # @ Description: used for extracting the rooms from the image (which I can't automate it, at the moment) and then combines the plot of the data with the heatmap.
 '''

import cv2
import os
import numpy as np
import PySimpleGUI as sg

# popup window for instructions


def popup():
    """
    Popup that explains how to select the rooms from the floor map.
    """
    understood = False
    layout = [[sg.Text('Seleziona una stanza trascinando il mouse da un angolo a quello opposto.\nUna volta selezionata la stanza, premi ENTER o SPAZIO, se commetti un errore, premi c.\nConclusa la selezione delle stanze in cui hai effettuato misure, premi ESC.')]]
    window = sg.Window('Istruzioni', layout)
    while not understood:                             # The Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            understood = True
            break


def get_rooms(imgname):
    """Select the rooms as ROIs by interaction of the user.

    Args:
        imgname (strin): path of the floor map.

    Returns:
        ndarray: array containing [x1,y1,x2,y2] for each room: 
            (x1,y1) - top left point of the room
            (x2,y2) - width and height of the room
    """
    [folder, name] = os.path.split(imgname)
    rooms_path = folder+'/rooms_'+name+'.npy'

    # selecting the regions of interest using the select ROIs function
    if os.path.isfile(rooms_path):
        # print(rooms_path+' found. Using coordinates previously selected.\n')
        rois = np.load(rooms_path)
    else:
        img = cv2.imread(imgname)
        room_selected = True
        popup()

        while room_selected:
            rois = cv2.selectROIs("Seleziona le stanze",
                                  img, showCrosshair=False)
            if len(rois):
                print("Hai individuato {} stanze".format(len(rois)))
                room_selected = False
            else:
                print("Devi selezionare almeno una stanza!")
        cv2.destroyAllWindows()  # close the window
        np.save(rooms_path, rois)

    return rois


def combine_plots(heatmap_paths, original_map, mode_name):
    """Puts the heatmaps on top of the floormap with transparency

    Args:
        heatmap_paths (array): array of strings containing the names of the heatmaps
        original_map (string): path of the floor map file
    """
    img = cv2.imread(original_map)
    [folder, floor_plan] = os.path.split(original_map)
    img_cpy = img.copy()
    for i in range(0, len(rooms_selection)):
        # print(heatmap_paths[i]);
        if os.path.isfile(heatmap_paths[i]):
            # reads also the alpha channel (the 4th)
            image_2 = cv2.imread(heatmap_paths[i], cv2.IMREAD_UNCHANGED)
            tl = np.asarray([rooms_selection[i, 0], rooms_selection[i, 1]])
            br = np.asarray([tl[0]+rooms_selection[i, 2],
                             tl[1]+rooms_selection[i, 3]])
            X, Y = np.abs(tl-br)
            # print("TopLeft coordinate {};\n BottomRight coordinate {}; \n Width = {}\n Height = {}".format(tl,br,X,Y))

        # Here, dsize accepts the dimensions to which the image is to be resized
            resized_image_2 = cv2.resize(image_2, dsize=(int(X), int(Y)))

        # Now, the non-white parts of the second image, are added to the original floor map:
            img[int(tl[1]):int(br[1]), int(tl[0]):int(br[0])] = img[int(tl[1]):int(br[1]), int(tl[0]):int(br[0])] * (1 - resized_image_2[:, :, 3:] / 255) + \
                resized_image_2[:, :, :3] * (resized_image_2[:, :, 3:] / 255)

    alpha = .6
    beta = 1-alpha
    # performs weighted sum of the images and saves it on top of the first one
    cv2.addWeighted(img_cpy, alpha, img, beta, 0, img)
    cv2.imwrite(folder+'/completed_'+mode_name+floor_plan, img)


def data2room(full_data, img_pathname):
    """Takes the floor map and associates the measurements with the rooms.

    Args:
        full_data (list): list of zipped coordinates and measure
        img_pathname (string): path of the floor map file

    Returns:
        list, array: 'room' containing the location of the measures inside each room and the measure itself,
                     'sizes' containing the size of the rooms
    """
    # Takes the clean image and evaluates the number and location of rooms via get_rooms;
    # next it assigns the points to the rooms
    global rooms_selection
    rooms_selection = get_rooms(img_pathname)
    sizes = np.zeros((len(rooms_selection), 2), dtype=int)
    # [folder,floor_plan] = os.path.split(img_pathname);
    # rooms_pathname = folder+'/roooms_'+floor_plan+'.npy';

    # if os.path.isfile(rooms_pathname):
    # print(rooms_pathname+' found. Using rooms previously created.\n')
    # room = np.load(rooms_pathname)
    # else:
    room_no = len(rooms_selection)
    full_data_no = len(full_data)
    room = [[] for _ in range(room_no)]
    for ind, val in enumerate(rooms_selection):
        tl = np.asarray([rooms_selection[ind, 0], rooms_selection[ind, 1]])
        br = np.asarray([tl[0]+rooms_selection[ind, 2],
                         tl[1]+rooms_selection[ind, 3]])
        sizes[ind] = np.asarray(br-tl)

    for items in full_data:
        # print(items)
        for ind, val in enumerate(rooms_selection):
            tl = np.asarray([rooms_selection[ind, 0], rooms_selection[ind, 1]])
            br = np.asarray([tl[0]+rooms_selection[ind, 2],
                             tl[1]+rooms_selection[ind, 3]])
            if items[0][0] >= tl[0] and items[0][0] <= br[0] and items[0][1] >= tl[1] and items[0][1] <= br[1]:
                room[ind].append((items[0]-[tl[0], tl[1]], items[1]))
                # print('room {}'.format(ind))
                break		# np.save(rooms_pathname,room)
    # print("Room {} \n sizes {}".format(room,sizes))
    return room, sizes
