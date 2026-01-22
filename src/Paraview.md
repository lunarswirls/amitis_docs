# Paraview Tricks and Tips

## Create a nice streamline plot:
1. Create a slice along a plane
2. On the new slice, select Filters > Merge Vector Components
3. In "Merge Vector Components" settings, select the settings to be whatever X, Y, Z components you want to represent as streamlines and color by magnitude of the vector
	1. For example, see magnetic field vector settings, where output vector is named "B_vector"
![merge_vector](/figs/merge_vector.png)
4. Once you have your new merged vector field, select Filters > Stream Tracer With Custom Source
5. On the window that pops up, choose "Seed Source" and choose your new merged vector field in the selection box
![seed_source](/figs/seed_source.png)
6. Once your streamlines have plotted, change the color to either a solid color or the magnitude of the vector field, depending on how you would like your visualization to look

## Plot surface flux
Each step creates a link in a pipeline, apply the next step to the most recent link in the pipeline so all fields are available
1. Create a sphere via Filters > Alphabetical > Slice then change Slice Type from default Plane to Sphere and set center to 0,0,0 and radius to your desired value
2. Calculate surface normals on sphere via Filters > Alphabetical > Surface Normals (function name may be different in older versions of Paraview but output is the same)
3. Group vector components of velocity into new named field via Filters > Alphabetical > Merge Vector Components
4. Calculate surface flux via Filters > Calculator and, replacing the brackets with your variable names, enter the formula:
	- dot({step3 vector name}, Normals) $\times$ {your density variable}
5. Visualize on sphere by scrolling down in calculator and choosing appropriate settings
![surface_flux_plot](/figs/surface_flux_plot.png)