# data2map
***data2map*** is a software that is supposed to take the measurements from an excel file, and plot them superimposed to the floormap of the office/space where the measurement has occurred.

The idea is the following:
 - measurements of either EOR (environmental optical radiation) or noise are performed and recorded into an excel file (.xcl or .xlsx) in a column;
 - the interface will guide you through the selection of the file (and the sheet) containing the measurements and the floormap;
 - on the floormap file (.png or .gif), one clicks on the PoM (point of measurement), i.e. the point at which the measurement is performed. Next to that point, highlighted with a red asterisc, a number will appear, that reprensents the row number (i-th measure on the i-th point -- easy, uh?). If an error is done in this phase, a right click will cancel the last point that will become blue;
 - select the type of data collected (OER or noise);
 - the software will finally create a floormap with a superimposed heatmap plot.

**At the moment**, the software needs some improvements, but some workaround are possible:

 - one has to pick a number of points that is equal to the number of measurements;
 - it is necessary to use it for *offices floormaps*, i.e. in environments that do not present shadowing (say, for example in warehouses or places where the noise-absorbption power of objects cannot be neglected);
 - in each room, one should pick *at least* 3 points. 

Future upgrade:
- [ ] make the PoM selection process smarter, closing the figure as soon as the number of measurements is reached;
- [ ] make the GUI nicer and clearer;
- [ ] enable one to use various floor maps, not only office-like ones;
- [ ] possible bug in the room count part of the code, where objects smaller than a certain amount are ignored.

# How to
Before launching the 'data2map.py' script, assuming all the packages needed are installed, the only requirement is that both the floormap and the excel file containing the data are in the same folder.

Once that is done, launch the script 'data2map.py' and follow the instructions.