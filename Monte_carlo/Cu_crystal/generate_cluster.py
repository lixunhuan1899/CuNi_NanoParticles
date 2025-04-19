import numpy as np
from ase.io import write
from ase import Atoms
import os
from tqdm import tqdm

a = 3.6147
d_min = 2.0
num_atoms = 5000
element = "Cu"

R = (a**3 / 4. * num_atoms * 3. / 4. / np.pi)**(1. / 3.)

pos = []
with tqdm(total=num_atoms, desc="Generating atoms", unit="atom") as pbar:
    while len(pos) < num_atoms:
        this_pos = (2. * np.random.rand(3) - 1) * R
        if np.linalg.norm(this_pos) > R:
            continue
        if pos:
            distances = np.linalg.norm(np.array(pos) - this_pos, axis=1)
            if np.all(distances >= d_min):
                pos.append(this_pos)
                pbar.update(1)
        else:
            pos.append(this_pos)
            pbar.update(1)

atoms = Atoms(f"{element}{num_atoms}", positions=pos, pbc=True)

#os.makedirs("init_xyz", exist_ok=True)
atoms.center(vacuum=6.0)
write("Cu_crystal/Cu_5000.xyz", atoms)




