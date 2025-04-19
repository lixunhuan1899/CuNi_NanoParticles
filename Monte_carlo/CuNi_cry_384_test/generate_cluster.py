import numpy as np
from ase.io import write
from ase import Atoms

a = 3.6147
d_min = 2.
append = False
num = 1
#nrand = 2
#f_Cu=0.5
f_Cu=[0.4]

for i in f_Cu:
    R = (a**3 / 4. * 384* 3. / 4. / np.pi)**(1. / 3.)
    pos = []
            
    while len(pos) < 384:
          this_pos = (2. * np.random.rand(3) - 1) * R
          if np.linalg.norm(this_pos) > R:
             continue
          if pos:
             distances = np.linalg.norm(np.array(pos) - this_pos, axis=1)
             if np.all(distances >= d_min):
                pos.append(this_pos)
          else:
              pos.append(this_pos)
           
    n_Cu = int(384 * i)
    n_Ni = 384 - n_Cu

    atoms = Atoms(f"Cu{n_Cu}Ni{n_Ni}", positions=pos, pbc=True)
    write("init_xyz/all.xyz", atoms, append=append)
    atoms.center(vacuum=6.)
    write(f"init_xyz/{i}.xyz", atoms)
    #num += 1
    append = True
