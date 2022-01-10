'''
 # @ Author: Enrico Martello
 # @ Create Time: 2022.01.10 11:34
 # @ Modified time: 2022.01.10 11:45
 # @ Description: plots the data as heatmaps.
 '''

import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt


def heatmap(room, room_size, is_light=True,out_name='interpolated.png'):

	x = np.zeros(len(room),dtype = int);
	y = np.zeros(len(room),dtype = int);
	z = np.zeros(len(room),dtype = int);
	# data coordinates and values
	for ind,val in enumerate(room):
		x[ind] = val[0][0]; y[ind] = val[0][1]; z[ind] = val[1];

	# target grid to interpolate to
	# print(room_size)
	xi = np.arange(0,room_size[0]+1,1); yi = np.arange(0,room_size[1]+1,1);
	xi,yi = np.meshgrid(xi,yi)

	# set mask
	mask = (xi > room_size[0]) & (xi < 0)  & (yi > room_size[1]) & (yi < 0) 

	# interpolate and mask out the field
	zi = griddata((x,y),z,(xi,yi),method='linear')
	zi[mask] = np.nan

	minimum = int(np.floor(np.amin(z) / 10.0)) * 10 ;
	maximum = int(np.ceil(np.amax(z) / 10.0)) * 10 ;

	cmap_selector = ['RdYlGn_r', 'RdYlGn'];

	# plot
	fig = plt.figure(frameon=False)
	# ax = fig.add_subplot(111)
	ax =plt.Axes(fig,[0.,0.,1.,1.])
	ax.set_axis_off()
	fig.add_axes(ax)
	plt.contourf(xi,yi,zi,np.arange(minimum,maximum,1),cmap=cmap_selector[is_light])
	plt.plot(x,y,'k.')
	plt.xlabel('xi',fontsize=16)
	plt.ylabel('yi',fontsize=16)
	# plt.colorbar()
	plt.savefig(out_name,dpi=100)
	# plt.close(fig)
	# plt.show()
	return out_name