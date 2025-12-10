To create a nice-ish streamline plot:
1. Create a slice along a plane
2. On the new slice, select Filters > Merge Vector Components
3. In "Merge Vector Components" settings, select the settings to be whatever X, Y, Z components you want to represent as streamlines and color by magnitude of the vector
	1. For example, see magnetic field vector settings, where output vector is named "B_vector"
![merge_vector](/figs/merge_vector.png)
4. Once you have your new merged vector field, select Filters > Stream Tracer With Custom Source
5. On the window that pops up, choose "Seed Source" and choose your new merged vector field in the selection box
![seed_source](/figs/seed_source.png)
6. Once your streamlines have plotted, change the color to either a solid color or the magnitude of the vector field, depending on how you would like your visualization to look
