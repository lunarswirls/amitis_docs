All input files and output logs are text

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

## Running a simulation
**NEVER RUN ANYTHING IN `home` DIRECTORY**
1. Go into active file storage space (see [HPC2N](HPC2N))
```
cd /proj/nobackup/amitis/
```
2. Go into your user subdirectory
```
cd /user/
```
3. Make a new folder (or select existing folder) for simulation you would like to run
	a. Shahab suggests 1 folder per simulation
```
mkdir /test/
```
4.  In `test` you should have at least 4 files:
	a. Amitis_exe. (could exist in top level folder, not required in each simulation directory)
	b. Amitis.inp (contains [required simulation variables](Amitis_Definitions.md))
		i. Can be edited during run! Change will be applied at next iteration and logged 
	c. Amitis.itr (contains [interior profile](Interior_file.md))
	d. submission file (`sub.sh`)
5. To place simulation in job queue, run `sub.sh` that contains [job definitions](Job_Script.md):
```
sbatch sub.sh
```
6. Check status of job(s):
```
squeue -u {user}
```
7. If you want to cancel a job:
```
scancel {job_id}
```

## Numerical Noise
- Can be resolved by changing $\Delta t$ or other tricks