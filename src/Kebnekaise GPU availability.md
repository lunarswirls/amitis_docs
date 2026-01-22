- Cannot mix GPU types!

| Number of nodes | GPU type | GPUs per node | RAM   |
| --------------- | -------- | ------------- | ----- |
| 1               | A6000    | 2             | 48 GB |
| 1               | A40      | 8             | 48 GB |
| 2               | L40S     | 8             | 48 GB |
| 12              | L40S     | 2             | 48 GB |
| 10              | V100     | 2             | 16 GB |


To choose which GPU to use one can use the command:

```
sinfo -N -t idle -o "%N %t %G"
```
which will return the idle nodes.
