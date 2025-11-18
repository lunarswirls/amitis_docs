# High Performance Computing Center North (HPC2N)
- Individual user accounts
- Login node is connected to compute nodes and file storage nodes, compute nodes and file storage nodes are connected (triangle)
- User only has access to login and file storage nodes, *no direct access to compute node*

```
ssh user@kebnekaise.hpc2n.umu.se
```

- Can enter password each time or set up config for user profile (shell is up to user)
- Each user has private `home` folder on file storage node with limited free space (~30 GB)

```
cd .../home/
```

- Project has `large_storage` subnode shared among all users split into ~40 TB active, 0.5 PB for archiving
	- Neither is backed up 
- Active file storage subnode path for Amitis is `/proj/nobackup/amitis/`
- Jobs are managed using [SLURM](https://slurm.schedmd.com/overview.html)
- Basic file browser and upload/download via [Cyberduck](https://cyberduck.io/)
