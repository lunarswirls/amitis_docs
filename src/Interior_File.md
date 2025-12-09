# Interior File

- Row format in *.itr file should not be changed!

The interior file is used to describe a bodies interior conductivity. An arbitrary example can be found here:
```
| X   | Y   | Z   | R_x      | R_y      | R_z      | eta     |
| [m] | [m] | [m] | [m]      | [m]      | [m]      | [Ohm-m] |
|-----|-----|-----|----------|----------|----------|---------|
| 0.0 | 0.0 | 0.0 | 2440.0e3 | 2440.0e3 | 2440.0e3 | 1.0e6   |
```
Where X,Y,Z describe the center of the conductivity source (currently at the origin) and R_x, R_y, R_z describe the radii of the sphere (currently a perfect sphere with radius of 2440 km). More complicated conductivity profiles can be defined such as a shell, which consists of three rows:
```
| X   | Y   | Z   | R_x      | R_y      | R_z      | eta   |

|-----|-----|-----|----------|----------|----------|-------|
| 0.0 | 0.0 | 0.0 | 2440.0e3 | 2440.0e3 | 2440.0e3 | 1.0e6 |
| 0.0 | 0.0 | 0.0 | 1940.0e3 | 1940.0e3 | 1940.0e3 | 2.0e6 |
| 0.0 | 0.0 | 0.0 |  940.0e3 |  940.0e3 |  940.0e3 | 1.0e6 |
```

Amitis then works its way from the outside overwriting conductivity values with later lines. In this case a shell reaches from 1940 - 2440 km, followed by e.g. a mantle region with conductivity of 2.0 S/m (940 - 1940 km) and the core from 0 - 940 km.

And even more complex geometries can be defined such as PKT but one must be careful defining regions of interest! 

## Common pitfalls

### Line breaks
Be careful editing this file, there should be no trailing line breaks, it will otherwise be read as a layer with a conductivity of 0, which will cause:

```
 <<< *ERR in task 0 >>> (validate:128) | Interior resistivity (0.000000e+00) for layer (2)
 Interior resistivity (0.000000e+00) for layer (2) should be larger than zero!
```

### Comments
You **can not** add any comments in this file, the code will produce the same error as above. 

### Resolution
To create several conductivity layers or shapes, keep in mind the resolution set for the grid cells. These should be at least two times smaller, such that the conductivity profile will be resolved. The higher the grid resolution the better.