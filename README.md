# data2map
This software takes noise or environmental optical radiation (EOR) measurements from an excel file, and plot them on top of the floormap of the office/space where the measurement has occurred.

The idea is the following:
 - measurements of either noise or EOR are performed and recorded into an excel file (`.xcl` or `.xlsx`) in a single column (see e.g. [here](./Test/test_data.xlsx));
 - the interface will guide you through the selection of the file (and the sheet) containing the measurements and the floormap;
 - on the floormap file (`.png` or `.gif`), one clicks on the point where the measurement occurred (PoM). Next to that point, highlighted with a red asterisc, a number will appear, that reprensents the row number (i-th measure on the i-th point -- easy, uh?). If an error is done in this phase, a right click will cancel the last point that will become cyan;
 - select the type of data collected (EOR or noise);
 - the software will finally create a floormap with a superimposed heatmap plot as shown below.
 
 ![completed_floormap](/Test/completed_Floormap.png )


**At the moment**, the software needs some improvements, for example:
 - it is necessary to use it for *offices floormaps*, i.e. in environments that do not present shadowing (say, for example in warehouses or places where the noise-absorbption power of objects cannot be neglected);
 - in each room, one should pick *at least* 4 points, otherwise those measurements will not be shown in a heatmap -- anyway, the user will se a warning about that;
 - if rooms are not the usual rectangular shape but, for example one is "L" shaped, then it is recommended that one uses a comlpeted floormap as the initial map, and prints the second set of measurements on top of the first ones.

 Also, I recommend taking measurements along the perimeter (and more importantly) at the corners of each room, so that the heatmap looks nicely fitting on top of the floormap.


Future upgrade:
- [x] make the GUI nicer and clearer;
- [x] possible bug in the room count part of the code, where objects smaller than a certain amount are ignored;
- [ ] make the figure close as soon as the number of selected PoM is reached;
	- [x] added countdown with the number of points left to be selected
- [ ] create launching script;
	- [x] added a guide on how to create a clickable script;
- [ ] enable picking floormaps and data from different folders;
- [ ] improve error messages and handling;
	- [ ] enable multiple languages
- [ ] enable one to use various floor maps, not only office-like ones;
- [ ] save EOR and noise maps on different files;
- [ ] popup for "I'm working on it";
- [ ] close selection data type popup after clicking "ok";


## Requirements
All the required packages are specified in `requirements.txt`. The script works with Python 3.8 (it has not been tested with different versions). At the moment, both the floormap and the excel file containing the measures have to be in the same folder.

# How to
Here is a quick guide on how to make the software run:
1. Open the terminal and navigate to the directory where the scripts are by typing: 
	```shell
	cd Folder/Containing/data2map/
	```
2. Install the required packages:
	```shell
	pip install -r requirements.txt
	```
3. If no error occurred, you can launch the `data2map.py` script by simply tiping:
	```shell
	python data2map.py
	```
	and hitting <kbd>ENTER</kbd>. Then follow the instructions.

Try it with the data in [this folder](./Test/).

# Creating a clickable script

It is also possible to create a clickable icon that automatically launches the script. Since the procedure depends on the operating system and I have only practiced it using MacOS, I will only describe that, but if you are using Ubuntu you probably want to refer to [this answer](https://askubuntu.com/questions/138908/how-to-execute-a-script-just-by-double-clicking-like-exe-files-in-windows), 
while on windows you probably want to read [these answers](https://stackoverflow.com/questions/37219045/windows-run-python-command-from-clickable-icon).

In order to create a clickable script named `data2map_launcher` on **Mac OS**, you have to go through the following steps:
1. open Terminal app, and type the following command: 
	```shell
	vim data2map_launcher
	```
	It will open up a text editor. Hit `i` nad you will enter insert mode. Be careful, you can only navigate the `vim` window by using arrows, clicks are useless :)

2. Type:
	```shell
	#!/bin/bash
	cd Folder/Containing/data2map/
	python data2map.py
	```
	You can obtain the path to the folder `data2map` by right clicking on its icon; while pressing on the <kbd>⌥</kbd> key, click on "Copy 'data2map' as pathname". Then you can paste the result into the `vim` shell by hitting <kbd>⌘ + v</kbd>.

3. Once you are done, hit <kbd>ESC</kbd> (to exit the insert mode), then `:wq` (to save and then quit the `vim` environment).

4. Still in the terminal type:
	``` shell
	chmod 700 data2map_launcher
	open .
	```
	and hit <kbd>Enter</kbd>. The first line will grant the script permission to read and execute the script to the user, the second line will open up the Finder right where the script was created.

5. Right-click on the file you have just created, select "Open with" and then "Other...", and select the application you want the file to execute, which is Terminal. In ase you are not able to select it, please switch from "Recommended Applications" to "All Applications", and is found in the Utilities folder.

6. **Optional step** if you want to personalise the icon of the script, open the image you want to use as an icon with Preview, hit File > Copy, then right-click on the script icon, then click on Get Info. In the new window that opens up, click on the logo right next to the name, and hit <kbd>⌘ + V</kbd>. I would be flattered if you used [this image](Test/suggested_icon.icns), but feel free to use the one that you like most.

# Updates & Upgrades

## Upgrade 04.02.22
- adding instruction to 'README.md' file on how to create a clickable script on MacOS
- adding a suggested icon
- adding a "Test" folder containing a floor map and an excel file with some random measurements

## Upgrade 13.01.21
- now the number of PoM to be selected on the floormap is shown in the top-left corner;
- fixed a bug that made the script crush for if less than 4 points are picked in a room;
- improved GUI and error handling if no file or floormap is selected; "Go" button has been removed.

## Upgrade 10.01.21
- `get_points` has been modified so that now, if the number of PoM is different than the number of measurements, the software does not stop working, yet it chops the longest of the two, and keeps working (after pointing out the issue);
- `room_borders` has been modified so that one can now select the rooms with a process explained in the popup -- works better for rectangular rooms, but there are smart workarounds;
- `requirements.txt` is the list of packages required in order to run the script (smoothly).  In order to install them all using `pip` type: ```pip install -r requirements.txt``` shouldn't it work, install them manually one by one (they are only 6, and probably some of them are already there). I am aware of only one issue with `tkinter` being too outdated, so in that case don't panic.