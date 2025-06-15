import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

time = np.array([1, 2, 3, 4])

surface_9A = np.array([174, 174, 171, 171])
inner_9A = np.array([66, 66, 69, 69])

surface_75A = np.array([202, 204, 201, 199])
inner_75A = np.array([38, 36, 39, 41])

plt.figure(figsize=(9, 6))

plt.plot(time, surface_9A, marker='o', linestyle='-', color='tomato', linewidth=2, label='Surface Cu (cutoff 9 Å)')
plt.plot(time, inner_9A, marker='^', linestyle='-', color='darkred', linewidth=2, label='Inner Cu (cutoff 9 Å)')
plt.plot(time, surface_75A, marker='s', linestyle='--', color='royalblue', linewidth=2, label='Surface Cu (cutoff 7.5 Å)')
plt.plot(time, inner_75A, marker='v', linestyle='--', color='navy', linewidth=2, label='Inner Cu (cutoff 7.5 Å)')


def annotate(x, y, color):
    for xi, yi in zip(x, y):
        plt.text(xi, yi + 2, str(yi), ha='center', fontsize=9, color=color)


annotate(time, surface_9A, 'tomato')
annotate(time, inner_9A, 'darkred')
annotate(time, surface_75A, 'royalblue')
annotate(time, inner_75A, 'navy')

plt.xlabel('Simulation Time (ns)', fontsize=12)
plt.ylabel('Number of Cu Atoms', fontsize=12)
plt.title('Cu Atomic Distribution', fontsize=14)

plt.xticks(time, fontsize=11)
plt.yticks(fontsize=11)
plt.ylim(0, max(surface_75A) + 20)
plt.grid(True, linestyle='--', alpha=0.6)

plt.legend(fontsize=11, loc='center', bbox_to_anchor=(0.5, 1.15), ncol=2)
plt.tight_layout()
plt.savefig("Cu_distribution_visual.png", dpi=300)
plt.show()
