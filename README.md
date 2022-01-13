# data2map
***data2map*** is a software that takes noise or environmental optical radiation measurements from an excel file, and plot them on top of the floormap of the office/space where the measurement has occurred.

The idea is the following:
 - measurements of either EOR (environmental optical radiation) or noise are performed and recorded into an excel file (.xcl or .xlsx) in a column;
 - the interface will guide you through the selection of the file (and the sheet) containing the measurements and the floormap;
 - on the floormap file (.png or .gif), one clicks on the PoM (point of measurement), i.e. the point at which the measurement is performed. Next to that point, highlighted with a red asterisc, a number will appear, that reprensents the row number (i-th measure on the i-th point -- easy, uh?). If an error is done in this phase, a right click will cancel the last point that will become blue;
 - select the type of data collected (EOR or noise);
 - the software will finally create a floormap with a superimposed heatmap plot.

**At the moment**, the software needs some improvements, but some workaround are possible:

 - one has to pick a number of points that is equal to the number of measurements;
 - it is necessary to use it for *offices floormaps*, i.e. in environments that do not present shadowing (say, for example in warehouses or places where the noise-absorbption power of objects cannot be neglected);
 - in each room, one should pick *at least* 3 points. 

Future upgrade:
- [ ] improve error messages and handling;
- [ ] make the PoM selection process smarter, closing the figure as soon as the number of measurements is reached;
- [x] make the GUI nicer and clearer;
- [ ] enable one to use various floor maps, not only office-like ones;
- [x] possible bug in the room count part of the code, where objects smaller than a certain amount are ignored. *10.01.21*

## Upgrade 10.01.21
- `get_points` has been modified so that now, if the number of PoM is different than the number of measurements, the software doesn't crash, yet it chops the longest of the two, and keeps working (after pointing out the issue);
- `room_borders` has been modified so that one can now select the rooms with a process explained in the popup -- Only works for rectangular rooms;
- `requirements.txt` is the list of packages required in order to run the script (smoothly).  In order to install them all using `pip` type: ```pip install -r requirements.txt``` shouldn't it work, install them manually one by one (they are only 6, and probably some of them are already there). I am aware of only one issue with `tkinter` being too outdated, so in that case don't panic.

## Upgrade 13.01.21
- now the number of PoM to be selected on the floormap is shown in the top-left corner;
- fixed a bug that made the script crush for if less than 4 points are picked in a room;
- improved GUI and error handling if no file or floormap is selected; "Go" button has been removed.

# How to
1 - Navigate to the directory where the scripts are, typing ```cd Folder/Containing/data2map/``` in the terminal.
2 - Install the required packages typing ```pip install -r requirements.txt```.
3 - If no error occurred, you can launch the `data2map.py` script by simply tiping ```python data2map.py``` and follow the instructions

## Requirements
All the required packages are specified in `requirements.txt`. The script works with Python 3.8 (it has not been teste with different versions). At the moment, both the floormap and the excel file containing the measures have to be in the same folder.