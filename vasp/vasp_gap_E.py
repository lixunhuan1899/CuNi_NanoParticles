import matplotlib.pyplot as plt
import numpy as np 


energy_file = ["energy_vasp.dat", "energy_gap.dat"]

energy=[]

for i in energy_file:
    with open(i, "r") as f:
        lines = f.readlines()
        data = list(map(lambda x: float(x.strip()) / 50, lines))
        energy.append(data) 

#error_list=[abs(a-b) for a,b in zip(energy[0],energy[1])]


#print(len(energy[0]))
#print(error_list)
print(energy)
min_val = min(min(energy[0]), min(energy[1]))
max_val = max(max(energy[0]), max(energy[1]))

x = [min_val, max_val]
y = [min_val, max_val]

plt.scatter(energy[0], energy[1], c="b",s=10)
plt.plot(x, y, linestyle="--", color="grey")

plt.xlabel("vasp energy (eV/atom)", fontsize=15)
plt.ylabel("gap energy (eV/atom)", fontsize=15)

plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

# plt.legend()
plt.tight_layout()
plt.savefig("./final_trail.png",dpi=300)
plt.show()
    
    
