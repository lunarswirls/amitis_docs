# Amitis Overview
- Amitis is three-dimensional in spatial and velocity components
- Cannot resolve electron scales, must stay on ion scales!
	- $\Delta l = min$($\Delta x$, $\Delta y$, $\Delta z$) $\gg \delta_e$ (i.e., $\Delta l \geq 10\delta_e$)

# Input file definitions
- Variable names in `*.inp` file should not be changed! 

## File Name
- Output file naming convention: `/out/Amitis_{fldname}_XXXXXX.h5`

## Object
- Center of body is always as center of simulation reference frame
- Object radius:
	- $obsr$ = 2440.0e3 [units: meters]

## Temporal Decomposition
- Time step calculated by $\Delta t \lt \frac{\mu_0 (\Delta l)^2}{(2\eta)}$ where $\Delta l$ = $min$($\Delta x$, $\Delta y$, $\Delta z$) and $\eta$ = $max$(inp_max($plsres$, $vacres$), itr_max($eta$))
	- $\Delta t$ = 0.001 [units: seconds]
- Total number of steps 
	- $numsteps$ = 100000 
- Total length of simulation = $numsteps$ * $\Delta t$

## Spatial Decomposition
- All units are SI
- Simulation domain cannot be defined by any geometry: accepted forms are cubes and rectangles
	- Spherical bodies are approximated by many cubes = sawtooth effect at limbs
- Cartesian coordinate system
- Simulation domain definitions:
	- $x_{min} \rightarrow x_{max}$ [units: meter]
	- $y_{min} \rightarrow y_{max}$ [units: meter]
	- $z_{min} \rightarrow z_{max}$ [units: meter]
- Grid cell geometry must be of similar form to domain
	- Recommended to choose cubic grid cells
- Grid cell definitions:
	- $nx \Rightarrow \Delta x$ = ($x_{max}$ - $x_{min}$) / $nx$
	- $ny \Rightarrow \Delta y$ = ($y_{max}$ - $y_{min}$) / $ny$
	- $nz \Rightarrow \Delta z$ = ($z_{max}$ - $z_{min}$) / $nz$
- Total number of grid cells = $nx$ * $ny$ * $nz$
![sim_domain_coordinates](figs/simulation_domain_coordinates.png)

## Computing Decomposition
- Specify number of GPUs to discretize simulation domain along each axis (recommended to be cubic)
	- $ngpux$ (should be divisible by $nx$)
		-  Recommend against using $ngpux$ > 1 due to computational cost of network communication between GPUs when particle traveling along X 
	- $ngpuy$ (should be divisible by $ny$)
	- $ngpuz$ (should be divisible by $nz$)
![gpu_domain_slice](figs/gpu_domain_slice.png)
- Per GPU, one cell is added to all sides of all axes
	- The "ghost cells" copy the closest cells from the neighboring GPU domain to hand off things that transition between GPU domains
- Example:
	- Discretization
		- $ngpux$ = 1
		- $ngpuy$ = 2
		- $ngpuz$ = 1
		- $nx$ = 20
		- $ny$ = 10
		- $nz$ = 10
	- Each GPU in Y gets 5 grid cells
	- Then GPU grid in Y-Z plane is actually 7 cells in Y and 12 cells in Z
![gpu_domain_ghost_cells](figs/gpu_domain_ghost_cells.png)
  
## Boundary Considerations
- Plasma always enter into Y plane at $x_{max}$ ("inflow boundary") and exits Y plane at $x_{min}$ ("outflow boundary")
	- Y planes are perfect absorbers, no propagation or periodicity
	- Define $vx$ as negative i.e. $vx$ = -400e3 [units: m/s]
![simulation_domain_velocity](figs/simulation_domain_velocity.png)
- Particles that exit the X and Z planes are reinjected to the opposite side, boundaries are periodic
- Electromagnetic fields are also periodic at boundaries so simulation domain must be chosen carefully so unwanted disturbances do not propagate across periodic boundaries
- Simulation domain cannot be made arbitrarily large without driving up computational cost

## Species Decomposition
- Definitions:
	- $numspecies$ = integer defining total number of particle species
- Definition per species i.e. proton:
	- $name$ = arbitary string 
	- $mass$ = 1.0 [units: not SI! amu]
	- $charge$ = 1.0 [units: not SI! UC]
	- $density$ = 5e6 [units: #/m^3]
	- $vx$ = -400e3 [units: m/s]
	- $vy$ = -20e3 [units: m/s] (prefer small values, for large values then rotate simulation domain)
	- $vz$ = -10e3 [units: m/s] (prefer small values, for large values then rotate simulation domain)
	- $T$ = 1.0e5 [units: K]
	- $ppc$ = 15 [units: not SI! integer number of particles in each grid cell at t=0]
	- $type$ = 0 or 1 [0: upstream plasma (default), 1: exospheric (or planetary plasma)]
- Distribution of all particles is Maxwellian (velocity bulk, temperature stdev)
- Total number of particles becomes
	- $tnp$ = $nx$ * $ny$ * $nz$ * $\sum_{i=1}^{\text{numspecies}} \text{ppc}_{i}$
	- $tnp\_percent$ = 0.05 [units: percent] (buffer for preallocation of $tnp$)
- Macroparticle approximation to reduce computation cost by only "moving" one particle that contributes an equal effect as moving the same particle density 
	- In the code, calculates pweight = (cell volume * density) / ppc
- If $numspecies$ < number of definitions per species, Amitis will ignore definitions after max($numspecies$)

## Dipole Moment
- If dipole does not exists, either set moment to 0 or comment out all lines
- Definitions:
	- $moment$ [units: A-m^2]
	- $dirx$ = 0.0 [units: not SI! can be anything, Amitis normalizes vector]
	- $diry$ =  0.0 [units: not SI! can be anything, Amitis normalizes vector]
	- $dirz$ =  0.0 [units: not SI! can be anything, Amitis normalizes vector]
	- $posx$ = 0.0 [units: m]
	- $posy$ = 0.0 [units: m]
	- $posz$ = 0.0 [units: m]
	- $period$ = 0 [TBD explanation]

## Crustal Field
**TBD**

## Solar Wind
- Definitions:
	- $Te$ = solar wind electron temperature [units: K]
- Interplanetary magnetic field
	- $Bx$ = 0.0e-9 [units: Tesla]
	- $By$ = 0.0e-9 [units: Tesla]
	- $Bz$ = +25.0e-9 [units: Tesla]
- Plasma resistivity:
	- $plsres$ = 1.0e4 [units: ohm-m]
	- $vacres$ = 2.0e6 [units: ohm-m]

## Writing Output
- Frequency at which to save output files
	- $fldsavecycle$ = 10 [units: number of steps] (0: off)
	- $parsavecycle$ = 0 [units: number of steps] (0: off)
	- $logstampcycle$ = 10 [units: number of steps] (0: off)
	- $rstcycle$ = 0 [units: number of steps] (0: off)
- Fields to write:
	- *fld\_save\_list* = unordered list of case-sensitive strings
		- Any subfield can be included or excluded, if string is not valid output field then **??**
		- Crustal fields and dipole fields are saved as $B_{d}$
		- Velocities not written directly, plasma current density output
		- Can get total charge density and per-species charge density (if you have only one species, only output $rho\_tot$)

# Interior file definitions
- Row format in `*.itr` file should not be changed! 

For a single conductivity profile, define one row
```
| X   | Y   | Z   | R_x      | R_y      | R_z      | eta   |
|-----|-----|-----|----------|----------|----------|-------|
| 0.0 | 0.0 | 0.0 | 2440.0e3 | 2440.0e3 | 2440.0e3 | 1.0e6 |
```

For a shell, define three rows 
```
| X   | Y   | Z   | R_x      | R_y      | R_z      | eta   |
|-----|-----|-----|----------|----------|----------|-------|
| 0.0 | 0.0 | 0.0 | 2440.0e3 | 2440.0e3 | 2440.0e3 | 1.0e6 |
| 0.0 | 0.0 | 0.0 | 1940.0e3 | 1940.0e3 | 1940.0e3 | 2.0e6 |
| 0.0 | 0.0 | 0.0 |  940.0e3 |  940.0e3 |  940.0e3 | 1.0e6 |
```

More complex geometries can be defined such as PKT but must be careful defining regions of interest! 
