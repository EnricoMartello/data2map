import data_master as dm
import get_points as gp
import room_borders as rb
import heatmapper as hm
import os
import numpy as np


def main(img_pathname, data_pathname):
	[folder,floor_plan] = os.path.split(img_pathname);

	# Once called, the function gets the measures from the excel sheet, and the coordinates from the click procedure
	measures = dm.select_sheet(data_pathname);
	# print("Measures are read correctly: {}".format(measures))
	gp.core(img_pathname);
	coordinates = np.load(folder+'/coords_'+floor_plan+'.npy');

	# Define the full_data list, ((X,Y),measure)
	full_data = list(zip(coordinates, measures));

	# Next, it takes the img_pathname, and looks for the "clean_img.png".
	# It is needed in order to look for the rooms, the measurements therein and their size.
	# cleanimg_pathname = folder + '/clean_'+ floor_plan;
	room, sizes = rb.data2room(full_data, img_pathname);
	# print("Room {} \n sizes {}".format(room,sizes))

	# Create the heatmaps
	heatmap_nameslist = ["" for i in range(len(room))];
	# print(heatmap_nameslist);print(type(heatmap_nameslist));
	light_vs_sound = dm.select_datatype();
	for i in range(0,len(room)):
		# print("len room[{}] = {}".format(i,len(room[i])))
		if (len(room[i])) != 0:
			heatmap_nameslist[i] = folder + '/room' + str(i+1) + floor_plan;
			# print(heatmap_nameslist[i])
			dummy = hm.heatmap(room[i],sizes[i],is_light=light_vs_sound,out_name=heatmap_nameslist[i]);
		else:
			print("Zero length for room[{}]. Room[{}] = {}".format(i,i,room[i]))
	
	# print("Combining plots...")
	rb.combine_plots(heatmap_nameslist,img_pathname);

	for i in range(0,len(room)):
		if os.path.isfile(heatmap_nameslist[i]):
			os.remove(heatmap_nameslist[i])


