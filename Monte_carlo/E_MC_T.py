import sys
import matplotlib.pyplot as plt
import numpy as np


with open("mc_E.log", "r") as f:
    lines = f.readlines()
    work_list = [line.split() for line in lines[1:]]
    energy_list=[]
    for row in work_list:
        if row[2] == "T":
           energy_list.append([int(row[0]), float(row[3])])
           
energy_list=np.array(energy_list)

max_step = np.max(energy_list[:, 0])  
min_E, max_E = np.min(energy_list[:, 1]), np.max(energy_list[:, 1])  

plt.figure(figsize=(10, 6))  
plt.plot(energy_list[:, 0], energy_list[:, 1], linewidth=1)  

plt.xlabel("Steps", fontsize=16)
plt.ylabel("E_mc(eV)", fontsize=16)
plt.title("Only true points",fontsize=16)

plt.ticklabel_format(style='sci', axis='both', scilimits=(0, 0))

plt.xticks(np.arange(0, max_step + 1, 3000), fontsize=16)  
plt.yticks(np.linspace(min_E, max_E, 10), fontsize=16)  


plt.grid(True, linestyle='--', alpha=0.6)

plt.savefig("mc_E_plot_T.png", dpi=300, bbox_inches='tight')


plt.show()