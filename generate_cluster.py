import numpy as np
from ase.io import write
from ase import Atoms

a = 3.6147
d_min = 2.
append = False
num = 1
nrand = 3

for f_Cu in np.arange(0., 1. + 1.e-10, 0.1):
    for i in range(nrand):
        R = (a**3 / 4. * 50* 3. / 4. / np.pi)**(1. / 3.)
        pos = []
            
        while len(pos) < 50:

              this_pos = (2. * np.random.rand(3) - 1) * R
              if np.linalg.norm(this_pos) > R:
                 continue
              if pos:
                 distances = np.linalg.norm(np.array(pos) - this_pos, axis=1)
                 if np.all(distances >= d_min):
                    pos.append(this_pos)
              else:
                 pos.append(this_pos)
           
        n_Cu = int(50 * f_Cu)
        n_Ni = 50 - n_Cu

        atoms = Atoms("Cu%iNi%i" % (n_Cu, n_Ni), positions=pos, pbc=True)
        write("init_xyz_CuNi_1/all.xyz", atoms, append=append)
        atoms.center(vacuum=6.)
        write("init_xyz_CuNi_1/%i.xyz" % num, atoms)
        num += 1
        append = True
