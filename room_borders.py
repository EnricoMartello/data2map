import cv2
import imutils, os
from imutils import perspective
import numpy as np
# removing small objects

# getting the rooms from the map

# clean_img_pathname = folder+'/clean_'+floor_plan; 
def get_rooms(imgname):
	img = cv2.imread(imgname)

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	font = cv2.FONT_HERSHEY_SIMPLEX
	_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

	mor_img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (3, 3), iterations=3)
	contours, hierarchy = cv2.findContours(mor_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # I addapted this part of the code. This is how my version works (2.4.16), but it could be different for OpenCV 3 

	sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
	area_list = []; box_list =[]
	for c in sorted_contours[1:]:
			area_list.append(cv2.contourArea(c))
	
	counter = int(0);

	for c in sorted_contours[1:]:
			area = cv2.contourArea(c)
			if area > 230000 and area < max(area_list):
				box = cv2.minAreaRect(c)
				box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
				box = np.array(box, dtype="int")

			# order the points in the contour such that they appear
			# in top-left, top-right, bottom-right, and bottom-left
			# order, then draw the outline of the rotated bounding
			# box
				box = perspective.order_points(box)
				box_list.append(box)
				
				# print(area);
				counter = counter+1
				# cv2.drawContours(img, [c], -1, (100, 100, 100), 10)
				# x, y, w, h = cv2.boundingRect(c) 
				# cx =int( x + w/2.); cy =int(y+h/2.); # for getting the approximate center of the rooms
				# cv2.putText(img,str(area),(cx,cy),font,0.5,(0,0,255),3)

	# print('I have spotted {} rooms'.format(counter))
	# cv2.imshow("mor_img", mor_img)
	# cv2.imshow("img", img)
	# cv2.waitKey(0)
	return box_list

def combine_plots(heatmap_paths,original_map):
	img = cv2.imread(original_map);
	[folder,floor_plan] = os.path.split(original_map);
	img_cpy = img.copy();
	for i in range(0,len(box_list)):
		# print(heatmap_paths[i]);
		if os.path.isfile(heatmap_paths[i]):
			image_2 = cv2.imread(heatmap_paths[i],cv2.IMREAD_UNCHANGED) #reads also the alpha channel (the 4th)
			tl = box_list[i][0]; br = box_list[i][2];
			X, Y = np.abs(tl-br);
			# print("TopLeft coordinate {};\n BottomRight coordinate {}; \n Width = {}\n Height = {}".format(tl,br,X,Y))
		
		# Here, dsize accepts the dimensions to which the image is to be resized
			resized_image_2 = cv2.resize(image_2, dsize=(int(X), int(Y)))
		
		# Now, the non-white parts of the second image, are added to the original floor map:
			img[int(tl[1]):int(br[1]),int(tl[0]):int(br[0])] = img[int(tl[1]):int(br[1]),int(tl[0]):int(br[0])] * (1 - resized_image_2[:, :, 3:] / 255) + \
                      																															resized_image_2[:, :, :3] * (resized_image_2[:, :, 3:] / 255) 

	alpha = .6;	beta = 1-alpha
	cv2.addWeighted(img_cpy, alpha, img, beta, 0, img) #performs weighted sum of the images and saves it on top of the first one
	cv2.imwrite(folder+'/completed_'+floor_plan,img)

def data2room(full_data, img_pathname):
	# Takes the clean image and evaluates the number and location of rooms via get_rooms;
	# next it assigns the points to the rooms
	global box_list
	box_list = get_rooms(img_pathname);
	sizes = np.zeros(len(box_list),dtype=type(box_list[0][0]))
	# [folder,floor_plan] = os.path.split(img_pathname);
	# rooms_pathname = folder+'/roooms_'+floor_plan+'.npy';

	# if os.path.isfile(rooms_pathname):
		# print(rooms_pathname+' found. Using rooms previously created.\n')
		# room = np.load(rooms_pathname)
	# else:
	room_no = len(box_list); full_data_no = len(full_data);
	room = [ [] for _ in range(room_no) ];
	for items in full_data:
		# print(items)
		for ind in range(0,room_no):
			tl = box_list[ind][0]; br = box_list[ind][2];		
			# print(tl); print(br)
			if items[0][0] >= tl[0] and items[0][0] <= br[0]:
				if items[0][1] >= tl[1] and items[0][1] <= br[1]:
					sizes[ind] = (br-tl)
					room[ind].append((items[0]-[tl[0], tl[1]],items[1]))
					# print('item');print(items)
					# print('room'); 
					# print(ind)
						# print('tl');print(tl)
					break;
		# np.save(rooms_pathname,room)
	# print("Room {} \n sizes {}".format(room,sizes))
	return room, sizes

# data= np.load('cleanmap.png_full.npy');
# combine_plots(image_2,get_rooms('/Users/enrico/Documents/PhD/extras/help_dad/clean_map.png'))
# print(rooms)

	
	