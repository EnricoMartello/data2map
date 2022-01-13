'''
 # @ Author: Enrico Martello
 # @ Create Time: 2022.01.10 11:34
 # @ Modified time: 2022.01.10 11:44
 # @ Description: Manages the selection of the PoM on the floor map.
 '''

# importing the module
import cv2
import os
import numpy as np

# function to display the coordinates of
# of the points clicked on the image
global coords, ind
coords = []


def click_event(event, x, y, flags, params):
    """records the position and  number of position selected on the floor map.

    Args:
        event (event): interaction event with the image
        x (int): x position of the click
        y (itn): y position of the click
    """
    marker = '*'
    countdown = "Punti rimasti da selezionare: "

    font = cv2.FONT_HERSHEY_SIMPLEX
    ((marker_width, marker_height), baseline) = cv2.getTextSize(marker, font, 1, 0)
    ((frame_w, frame_h), baseline) = cv2.getTextSize(countdown+"100", font, 1, 0)

    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # print('coord: ');print(x, ' ', y) # displaying the coordinates on the Shell
        # print('length = ');print(len(coords))
        # displaying the coordinates on the image window
        coords.append((x, y))
        pointer = marker + str(len(coords))
        cv2.rectangle(img, (0, 0), (frame_w, frame_h+40),
                      (255, 0, 255), thickness=-1)
        cv2.putText(img, countdown+str(n_max-len(coords)),
                    (0, 40), font, 1, (0, 0, 0), 2)
        cv2.putText(img, pointer, (x-int(marker_width/2), y +
                                   int(marker_height/2)), font, 1, (0, 0, 255), 2)
        cv2.imshow('image', img)

    # checking for right mouse clicks
    if event == cv2.EVENT_RBUTTONDOWN:  # EVENT_RBUTTONDBLCLK
        x0, y0 = coords[len(coords)-1]
        cv2.putText(img, marker, (x0-int(marker_width/2), y0 +
                                  int(marker_height/2)), font, 1, (255, 255, 0), 2)
        coords.pop()
        cv2.imshow('image', img)

    np.save(coords_path, coords)


def core(filename, n=0):
    """function that gets the points of measure on the floor map.

    Args:
        filename (string): path of the floor map
        n (int, optional): total number of measures. Defaults to 0.
    """
    global coords_path, n_max
    # ? Does n do anything?
    n_max = n
    # reading the image
    # print('---CORE HERE---')
    [folder, floor_plan] = os.path.split(filename)

    global img
    img = cv2.imread(folder+'/'+floor_plan, 1)
    coords_path = folder+'/coords_'+floor_plan+'.npy'

    if os.path.isfile(coords_path):
        # print(coords_path+' found. Using coordinates previously selected.\n')
        coords = np.load(coords_path)
    else:
        height = 780
        (h, w) = img.shape[:2]
        ratio = height/float(h)
        resize = cv2.resize(img, (int(ratio*w), height),
                            interpolation=cv2.INTER_AREA)
        cv2.imshow('image', img)  # displaying the image
        # setting mouse hadler for the image and calling the click_event() function
        cv2.setMouseCallback('image', click_event)
        cv2.waitKey(0)  # wait for a key to be pressed to exit
        cv2.destroyAllWindows()  # close the window
