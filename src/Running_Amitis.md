All input files and output logs are text

## Amitis Executable Inputs
- Amitis.inp -> main input file containing [required simulation variables](Amitis_Definitions.md)
	- Can be edited during run! Change will be applied at next iteration and logged 
- Amitis.itr -> interior profile

## Job requirements
- Submission file

## Generated folders
- /log/ -> log file per GPU at every X number of time steps
- /out/ -> hdf5 containing nicely formatted output
	- Output can contain particle and field files (separate) based on input flags
		- Can specify what to contain for each file type
- /rst/ -> hdf5 containing unformatted binary output with checksum at every X number of time steps to restart (can be TBs so be judicious in selecting X)
### Depend on input settings
- /planes/
- /subsets/
- /observers/