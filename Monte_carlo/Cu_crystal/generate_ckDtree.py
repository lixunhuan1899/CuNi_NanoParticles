import numpy as np
from ase import Atoms
from ase.io import write
from scipy.spatial import cKDTree

# 参数设置
r = 3.6147
num_atoms = 1000  # 目标数量
a = (r**3 / 4. * num_atoms * 3. / 4. / np.pi)**(1. / 3.)  # 球体半径
d_min = 2 # 最小距离
element = 'Cu'

# 估算需要多采样的倍数
sample_factor = 10
n_sample = num_atoms * sample_factor

# 在球内批量采样
positions = []
while True:
    xyz = np.random.uniform(-a, a, size=(n_sample, 3))
    r = np.linalg.norm(xyz, axis=1)
    mask = r <= a
    pos_in_sphere = xyz[mask]
    if len(pos_in_sphere) >= num_atoms:
        break

# 用 KDTree 快速筛选出满足距离限制的子集
tree = cKDTree(pos_in_sphere)
pairs = tree.query_pairs(d_min)

# 构建图（邻接点）
from collections import defaultdict

neighbors = defaultdict(set)
for i, j in pairs:
    neighbors[i].add(j)
    neighbors[j].add(i)

# 贪心法选择一组互不接近的点
selected = []
used = set()
for i in range(len(pos_in_sphere)):
    if i in used:
        continue
    selected.append(i)
    used.update(neighbors[i])
    used.add(i)
    if len(selected) >= num_atoms:
        break

if len(selected) < num_atoms:
    raise RuntimeError("采样不足以生成目标数量的原子，请增加 sample_factor 或减小 d_min")

final_positions = pos_in_sphere[selected[:num_atoms]]

# 构建原子结构并保存
symbols = [element] * num_atoms
atoms = Atoms(symbols=symbols, positions=final_positions)
atoms.center(vacuum=6.0)
write(f'{element}_sphere.xyz', atoms)

print(f"✅ 生成完成，共 {len(atoms)} 个原子，文件已保存。")
