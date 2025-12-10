#!/usr/bin/env python
# -*- coding: utf-8 -
# Imports:
import numpy as np
import os
import xarray as xr
import matplotlib.pyplot as plt

# change this to wherever you want your output figures to be saved
outdir = "/Users/danywaller/Projects/mercury/rps_cps_comparison/"
os.makedirs(outdir, exist_ok=True)  # creates directory if it doesnt already exist

# change this to your input directory
indir = "/Users/danywaller/Projects/mercury/"

# first stable timestamp approx. 25000 for dt=0.002, numsteps=115000
sim_steps = list(range(27000, 115000 + 1, 1000))

for sim_step in sim_steps:
    filename = 'Base_' + "%06d" % sim_step

    f1 = indir + "RPS_Base/object/Amitis_RPS_" + filename + "_xz_comp.nc"
    f2 = indir + "CPS_Base/object/Amitis_CPS_" + filename + "_xz_comp.nc"

    # --- Load files ---
    ds1 = xr.open_dataset(f1)
    ds2 = xr.open_dataset(f2)

    tot_den_rps = ds1["den01"].sel(Ny=0, method="nearest")
    tot_den_cps = ds2["den01"].sel(Ny=0, method="nearest")

    varnames = ["den02", "den03", "den04"]

    # --- Extract x–z plane at y = 0 and sum ---
    for var in varnames:
        tot_den_rps += ds1[var].sel(Ny=0, method="nearest")
        tot_den_cps += ds2[var].sel(Ny=0, method="nearest")

    # --- Subtract the planes ---
    difference = tot_den_rps - tot_den_cps

    # Extract metadata from either dataset (ds1 and ds2 should have same extent)
    xmin = float(ds1.full_xmin)
    xmax = float(ds1.full_xmax)
    zmin = float(ds1.full_zmin)
    zmax = float(ds1.full_zmax)

    dx = float(ds1.full_dx)
    dz = float(ds1.full_dz)

    # Build coordinate arrays
    x = np.arange(xmin, xmax + dx/2, dx)   # inclusive upper bound
    z = np.arange(zmin, zmax + dz/2, dz)

    x = x/2440.e3  # convert to R_m
    z = z/2440.e3

    data = difference.squeeze().values  # remove singleton dimension

    fig, ax = plt.subplots(figsize=(8, 6))
    plt.pcolormesh(x, z, data, vmin=0, vmax=100, shading='auto', cmap='ocean_r')
    circle = plt.Circle((0, 0), 1, edgecolor='black', facecolor='darkorange', alpha=0.3, linewidth=1,)
    ax.add_patch(circle)
    plt.xlabel(r"$\text{X (R}_{M}\text{)}$")
    plt.ylabel(r"$\text{Z (R}_{M}\text{)}$")
    plt.title(f"Total Density Difference at y = 0, t = {sim_step*0.002} seconds")
    plt.colorbar(label="Total Density Difference (RPS - CPS)")
    plt.tight_layout()
    fig_path = os.path.join(outdir, f"tot_den_diff_{sim_step}.png")
    plt.savefig(fig_path, dpi=300)