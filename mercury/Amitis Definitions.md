3D in spatial configuration and velocity
Some percent of university heating comes from computing center

## Object
- Center of body is always as center of simulation reference frame
- Definitions:
	- Object radius = 2440e3 [units: meters]

## Temporal Decomposition
- Iterative solver definitions:
	- Total number of steps = 100000 
	- Timestep delta t = 0.001 [units: seconds]
- Total number of steps * delta t = total length of simulation

## Spatial Decomposition
- All units are SI
- Simulation domain cannot be defined by any geometry: accepted forms are cubes and rectangles
	- Spherical bodies are approximated by many cubes = sawtooth effect at limbs
- Cartesian coordinate system
- Simulation domain definitions:
	- x_min -> x_max [units: meter]
	- y_min -> y_max [units: meter]
	- z_min -> z_max [units: meter]
- Grid cell geometry must be of similar form to domain
	- Recommended to choose cubic grid cells
- Grid cell definitions:
	- nx => delta x = (x_max - x_min) / nx
	- ny => delta y = (y_max - y_min) / ny
	- nz => delta z = (z_max - z_min) / nz
- Total number of grid cells = nx * ny * nz

## Computing Decomposition
- Specify number of GPUs to discretize simulation domain along each axis
	- ngpux (should be divisible by nx)
		-  Recommend against using ngpux > 1 due to computational cost of network communication between GPUs when particle traveling along X 
	- ngpuy (should be divisible by ny)
	- ngpuz (should be divisible by nz)
- Recommended to be cubic
- Per GPU, one cell is added to all sides of all axes
- Example:
	- Discretization
		- ngpux = 2
		- ngpuy = 1
		- ngpuz = 1
		- nx = 10
		- ny = 20
		- nz = 30
	- Each GPU in X gets 5 grid cells
	- Then GPU grid in X-Z plane is actually 7 cells in X and 32 cells in Z
- The "ghost cells" copy the closest cells from the neighboring GPU domain to hand off things that transition between GPU domains

## Boundary Considerations
- Plasma always enter along -X hat into Y plane ("inflow boundary") and exits Y plane in -X hat ("outflow boundary")
	- Define vx as negative i.e. vx = -400e3 [units: m/s]
- Particles that exit the X and Z planes are reinjected to the opposite side, boundaries are periodic
- Electromagnetic fields are also periodic at boundaries so simulation domain must be chosen carefully so unwanted disturbances do not propagate across periodic boundaries
- Simulation domain cannot be made arbitrarily large without driving up computational cost

## Species Decomposition
- Definitions:
	- numspecies
- Definition per species i.e. proton:
	- mass = 1.0 [units: not SI! just arbitrary]
	- charge = 1.0 [units: not SI! just arbitrary]
	- density = 5e6 [units: #/m^3]
	- vx = -400e3 [units: m/s]
	- vy = -20e3 [units: m/s] (prefer small values, for large values then rotate simulation domain)
	- vz = -10e3 [units: m/s] (prefer small values, for large values then rotate simulation domain)
	- T = 1.0e5 [units: K]
	- ppc = 15 [units: not SI! integer number of particles in each grid cell at t=0]
- Distribution of all particles is Maxwellian (velocity bulk, temperature stdev)
- Total number of particles becomes
	- tnp = nx * ny * nz * sum from i=1 to numspecies over ppc_i
- Macroparticle approximation to reduce computation cost by only "moving" one particle that contributes an equal effect as moving the same particle density 
	- In the code, calculates pweight = (cell volume * density) / ppc
