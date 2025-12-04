import pyamitis.version
from pyamitis.amitis_netcdf import *
from pyamitis.amitis_hdf import *


from pathlib import Path
import re
import os

cwd = os.path.dirname(os.path.realpath(__file__))
base_dir = Path(cwd+"/Data")
print(base_dir)

# All files in base_dir matching Amitis_field*.h5 (non‑recursive)
file_paths = sorted(base_dir.glob("Amitis_field*.h5"))

for path in file_paths:
    compress = True
    filename = path.stem

    obj_hdf = amitis_hdf(str(base_dir) + "/", filename+".h5")

    # extract exactly 6 digits after "field_"
    m = re.search(r"field_(\d{6})", filename)  # [web:51][web:53]
    if not m:
        raise ValueError(f"Could not extract sim_step from {filename!r}")

    sim_step = int(m.group(1))

    #####################################################
    # PRINT SOME ATTRIBUTES
    #####################################################

    # Print version
    pyamitis.version()

    # original dimensions  of the simulation domain
    original_domain = obj_hdf.get_hdf_domain()

    # print all attributes with their values
    obj_hdf.print_all_attributes()

    # print mean charge and mean mass of all species
    print(f'Mean charge of all species {obj_hdf.get_mean_charge()}')
    print(f'Mean mass   of all species {obj_hdf.get_mean_mass()}  ')

    # Since we start the for-loop from 1, we need to increment stop range
    for s in range(1, obj_hdf.get_num_species()+1):
        print('Specie %d mass = %.2e   charge = %.2e' %(s, obj_hdf.get_mass(s), obj_hdf.get_charge(s)) )
        print('Specie %d density = %.2e   v = (%.2e, %.2e, %.2e)' %(s, obj_hdf.get_density(s), obj_hdf.get_vx(s), obj_hdf.get_vy(s), obj_hdf.get_vz(s)) )
        print('===================================')

    #####################################################
    # READ DATASETS AND CONVERT THEIR UNITS
    #####################################################

    ores = obj_hdf.load_dataset('ores')
    dres = obj_hdf.load_dataset('dres')

    bx  = obj_hdf.load_dataset('Bx', 1.0e9)
    by  = obj_hdf.load_dataset('By', 1.0e9)
    bz  = obj_hdf.load_dataset('Bz', 1.0e9)

    bmag = np.sqrt(bx**2 + by**2 + bz**2)

    Ex  = obj_hdf.load_dataset('Ex', 1.0e3)   # (V/m) => (mV/m)
    Ey  = obj_hdf.load_dataset('Ey', 1.0e3)
    Ez  = obj_hdf.load_dataset('Ez', 1.0e3)
    Emag = np.sqrt(Ex**2 + Ey**2 + Ez**2)

    # Charge density and plasma number density
    rho_tot = obj_hdf.load_dataset('rho_tot')    # Total Charge Density: qn
    den_tot = rho_tot*1.e-6 / obj_hdf.get_mean_charge()   # calculating total number density in units of [#/cm^3]

    # Calcluate total plasma velocity
    jix = obj_hdf.load_dataset('jix_tot')   # rho_tot * vx
    jiy = obj_hdf.load_dataset('jiy_tot')   # rho_tot * vy
    jiz = obj_hdf.load_dataset('jiz_tot')   # rho_tot * vz


    bx_unitvec, by_unitvec, bz_unitvec = bx/bmag, by/bmag, bz/bmag
    
    vx  = jix*1.e-3 / rho_tot     # (m/s) => (km/s)
    vy  = jiy*1.e-3 / rho_tot
    vz  = jiz*1.e-3 / rho_tot
    vmag = np.sqrt(vx**2 + vy**2 + vz**2)

    # Electric current density from Ampere's law
    Jx = obj_hdf.load_dataset('Jx', 1.0e9)  # (A/m^2) => (nA/m^2)
    Jy = obj_hdf.load_dataset('Jy', 1.0e9)
    Jz = obj_hdf.load_dataset('Jz', 1.0e9)
    Jmag = np.sqrt(Jx**2 + Jy**2 + Jz**2)

    J_par = Jx*bx_unitvec + Jy*by_unitvec + Jz*bz_unitvec # field-aligned current density

    #####################################################
    # WRITE INTO A NETCDF FILE
    #####################################################
    # Open, write, and close netcdf file with real data
    # Comparison with original data file by eye for example with Panoply
    obj_netcdf = amitis_netcdf(obj_hdf.file_path, filename + '.nc', sim_step, 
                            original_domain, 
                            compression=compress) #, trimmed_domain)
    obj_netcdf.open()
    obj_netcdf.write_hdf_attributes(obj_hdf)

    obj_netcdf.write(ores     , 'ores'     , 'Ohm.m')
    obj_netcdf.write(dres     , 'dres'     , 'Ohm.m'  )

    obj_netcdf.write(bx      , 'Bx'      , 'nT'  )
    obj_netcdf.write(by      , 'By'      , 'nT'  )
    obj_netcdf.write(bz      , 'Bz'      , 'nT'  )
    obj_netcdf.write(bmag    , 'Bmag'    , 'nT'  )

    obj_netcdf.write(den_tot , 'den_tot' , 'cm-3')

    obj_netcdf.write(vx      , 'vx_tot'  , 'km/s')
    obj_netcdf.write(vy      , 'vy_tot'  , 'km/s')
    obj_netcdf.write(vz      , 'vz_tot'  , 'km/s')
    obj_netcdf.write(vmag    , 'vmag'    , 'km/s')

    obj_netcdf.write(Jx      , 'Jx'      , 'nA/m^2'  )
    obj_netcdf.write(Jy      , 'Jy'      , 'nA/m^2'  )
    obj_netcdf.write(Jz      , 'Jz'      , 'nA/m^2'  )
    obj_netcdf.write(Jmag    , 'Jmag'    , 'nA/m^2'  )
    obj_netcdf.write(J_par, 'J_par', '?')

    obj_netcdf.write(Ex      , 'Ex'      , 'mV/m'  )
    obj_netcdf.write(Ey      , 'Ey'      , 'mV/m'  )
    obj_netcdf.write(Ez      , 'Ez'      , 'mV/m'  )
    obj_netcdf.write(Emag    , 'Emag'    , 'mV/m'  )

    obj_netcdf.close()

print('Done!')