# Job Script
- All SBATCH commands require a hashtag in front of them
- To comment out a line, put 2+ hashtags
```
#!/bin/bash
#SBATCH A hpc2n2025-191  # project number
###SBATCH -N 1  # Number of nodes
#SBATCH -n 1  # Number of GPUs
#SBATCH --time:168:00:00  # do not set as the maximum time if you know it will take less time!! higher estimates can push you down the queue priority list
#SBATCH --gpus-per-node:140s:1  # possible types: v100 (16 GB; double precision), a6000 (48 GB; single precision, active cooling), a40 (48 GB; single precision, passive cooling), a140s (48 GB; single precision, passive cooling, more modern), a100 (48 GB; double precision)

###SBATCH --exclusive
#SBATCH --error=job_%J.err
#SBATCH --output=job_%J.out

# Clear the environment from any previously loaded modules
module purge > /dev/null 2>&1
ml gompi/2023b UCX-CUDA/1.15.0-CUDA-12.4.0 HDF/1.14.3

export OMPI_MCA_opal_cuda_support=True
srun Amitis 250116
```

- Number of GPUs ($ngpu_{total}$) should be equal to $ngpux * ngpuy + ngpuz$ in the [Amitis input file](Amitis_Definitions.md).
- On kebnekaise, each node has 2 GPUs so number of nodes should be $\lceil ngpu_{total} / 2 \rceil$
- A rough estimate for number of GPUs on kebnekaise is
$$ nx*ny*nz*(\text{sum of ppc for all species})*tnp_{percent} / ngpu_{total} = 600,000,000 $$