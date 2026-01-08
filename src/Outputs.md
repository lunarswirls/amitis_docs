# Conventions for the output of Amitis

The output file consists of many different physical quantities. As a way to standardize our work, we here present the raw outputs and their units.

## Fields

| Field                         | Input name       | Unit   | Comment       |
|-------------------------------|------------------|--------|---------------|
| Charge density p. species     | rho1, rho2, ...       | e/m^3  |               |
| Total charge density          | rho_tot          | e/m^3  |               |
| Electric current density      | jix, jiy, jiz         | A/m^2? | From momentum |
| Tot. Electric current density | jix_tot, jiy_tot, jiz_tot | A/m^2? | From momentum |
| Electric current density      | Jx, Jy, Jz       | A/m^2  | From Ampère   |
| Magnetic field                | Bx, By, Bz           | T      |               |
| Dipole Magnetic field         | Bdx, Bdy, Bdz         | T      |               |
| Crustal Magnetic field        | Bux, Buy, Buz         |       |               |
| Electric field.               | Ex, Ey, Ez           | V/m    |               |
| Dynamic resistivity           | dres             | Ohm/m  |               |
| Object  resistivity           | ores             | Ohm/m  |               |

### Computed quantities
To be added later


## Particles


## Attributes

| Field                     | Input name | Unit | Comment                                           |
| ------------------------- | ---------- | ---- | ------------------------------------------------- |
| Obstacle radius           | obs_radius | m   |   |
| Grid cells in x-direction | nx         | –    | Number of grid points along x       |
| Grid cells in y-direction | ny         | –    | Number of grid points along y       |
| Grid cells in z-direction | nz         | –    | Number of grid points along z       |
| Minimum x                 | xmin       | m    | Lower domain boundary in x          |
| Maximum x                 | xmax       | m    | Upper domain boundary in x          |
| Minimum y                 | ymin       | m    | Lower domain boundary in y          |
| Maximum y                 | ymax       | m    | Upper domain boundary in y          |
| Minimum z                 | zmin       | m    | Lower domain boundary in z          |
| Maximum z                 | zmax       | m    | Upper domain boundary in z          |