# Running Amitis
- All input files and output logs are text
- Output data files are [Hierarchical Data Format (HDF)](https://en.wikipedia.org/wiki/Hierarchical_Data_Format)

## Generated folders
- /log/ -> log file per GPU at every X number of time steps
- /out/ -> HDF5 files containing nicely formatted output
	- Output can contain particle and field files (separate) based on input flags
		- Can specify what to contain for each file type
- /rst/ -> HDF5 files containing unformatted binary output with checksum at every X number of time steps to restart (can be TBs so be judicious in selecting X)
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
	- Amitis_exe. (could exist in top level folder, not required in each simulation directory)
	- Amitis.inp (contains [required simulation variables](Amitis_Definitions.md))
		- Can be edited during run! Change will be applied at next iteration and logged 
	- Amitis.itr (contains [interior profile](Interior_file.md))
	- submission file (`sub.sh`)
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
8.
After a job has been submitted and is running, the resource monitor can be accessed via:
```
job-usage {job-id}
```
which results in a link to Grafana which shows showing all the resources of HPC2N that are used. An example can be found [here](https://usage.hpc2n.umu.se/d/job-on-kebnekaise-gpu?var-jobid=35369534&from=1763561221000&to=1763563788000). An explanation can be seen under [resource-monitor](resource-monitor.md).

## Restart Files
- Restart files are saved in your output directory under a new folder labeled `/rst/`
- If you need to restart a simulation, in your input file, define $rst=1$ and $rstname$ as the file **stem** in your `/rst/` dir (not the full file path!)
	- If you use multiple GPUs, each restart file will have a GPU ID appended to the name, e.g. Amitis_rst_045000_*G000*.h5, Amitis_rst_045000_*G001*.h5 but you need to declare only the stem as Amitis_rst_045000.h5 in the input file to restart
- Example:
```
# =============================================================================
# Restart configuration
# =============================================================================

rst        = 1
rstname    = ./rst/Amitis_rst_045000.h5
```

## Numerical Noise
- Can be resolved by changing $\Delta t$ or other tricks
- 