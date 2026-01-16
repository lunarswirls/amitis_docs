# Equations
- Useful definitions
## Electron Inertial Length
$\delta_e = \frac{c}{\omega_{p_e}}$

Plot $\delta_{e,i}$ as a function of density $n_{e,i}$

| Object   | n_p [cm^-3] | 
|----------|-------------|
| Mercury  | 40          | 
| Moon     |  5          | 
| Mars     |  2          | 
| Ganymede |  8          | 
| Europa   | 30          |

## Time step constraints
To find the maximal possible time step, that can be used before the simulation becomes unstable:

$\Delta t \lt \frac{\mu_0 (\Delta l)^2}{(2\eta)}$
where $\Delta l$ = $min$($\Delta x$, $\Delta y$, $\Delta z$) is the minimal cell size length, and $\eta$ is the maximum resistivity out of:
- plasma res.
- vacuum res.
- interior res.

## Charge Density
$\rho=qn \Rightarrow n = \frac{q}{\rho}$


## Useful script
A [python notebook](UsefulScript.ipynb) can also be found to compute these equations.
