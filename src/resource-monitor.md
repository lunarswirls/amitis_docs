# Resource Monitor

This page shall explain the ```job-usage``` Dashboard

It consists of 7 bullet points:
- CPU Utilization
- RAM Usage (Memory)
- Disk Memory ($TMPDIR)
- Lustre MDS
- Lustre OSS
- Pressure
- GPU

Since the GPU is used for all of the calculations in Amitis, this is the most important resource to monitor. 

## GPU

The GPU shows the **mean** GPU usage. Since the workload is divided symmetricly this can be seen as per GPU, however in some cases that might differ (e.g. GPUs with different VRAM). The most important part here is the Memory Usage, that should ideally between 80% as the mean, while the maximum usage can bump up to 95%. 