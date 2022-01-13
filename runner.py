'''
 # @ Author: Enrico Martello
 # @ Create Time: 2022.01.10 11:34
 # @ Modified time: 2022.01.10 11:45
 # @ Description: core of the softwware, manages the steps.
 '''

import data_master as dm
import get_points as gp
import room_borders as rb
import heatmapper as hm
import os
import numpy as np


def main(img_pathname, data_pathname):
    """Core of the software

    Args:
        img_pathname (string): path of the floor map
        data_pathname (string): path of the data file
    """
    [folder, floor_plan] = os.path.split(img_pathname)

    # * Once called, the function gets the measures from the excel sheet, and the coordinates from the click procedure
    print("*** Reading measures...")
    measures = dm.select_sheet(data_pathname)
    gp.core(img_pathname, n=len(measures))
    coordinates = np.load(folder+'/coords_'+floor_plan+'.npy')

    # * Define the full_data list, ((X,Y),measure)
    if len(coordinates) == len(measures):
        full_data = list(zip(coordinates, measures))
    else:
        print("Warning: you selected {} points for {} measurements.".format(
            len(coordinates), len(measures)))
        cutoff = min(len(coordinates), len(measures))
        full_data = list(zip(coordinates[:cutoff], measures[:cutoff]))

    # * It is needed in order to look for the rooms, the measurements therein and their size.
    print("*** Obtaining rooms...")
    room, sizes = rb.data2room(full_data, img_pathname)

    # print("Room {} \n sizes {}".format(room,sizes))

    # * Create the heatmaps
    print("*** Creating heatmaps...")
    heatmap_nameslist = ["" for i in range(len(room))]
    # print(heatmap_nameslist);print(type(heatmap_nameslist));
    light_vs_sound = dm.select_datatype()
    for i in range(0, len(room)):
        # print("len room[{}] = {}".format(i,len(room[i])))
        if (len(room[i])) > 3:
            heatmap_nameslist[i] = folder + '/room{}'.format(i+1) + floor_plan
            # print(heatmap_nameslist[i])
            dummy = hm.heatmap(
                room[i], sizes[i], is_light=light_vs_sound, out_name=heatmap_nameslist[i])
        else:
            print("Need more measures for room[{}] = {}".format(i+1, room[i]))

    print("Combining plots...")
    rb.combine_plots(heatmap_nameslist, img_pathname)

    for i in range(0, len(room)):
        if os.path.isfile(heatmap_nameslist[i]):
            os.remove(heatmap_nameslist[i])
