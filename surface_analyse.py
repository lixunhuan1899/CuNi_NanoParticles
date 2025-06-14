import numpy as np
from ase.io import read


def read_position(xyz_filepath: str) -> dict:
    position = {}
    with open(xyz_filepath, 'r') as f:
        lines = f.readlines()[2:]
        atoms = [line.split()[:4] for line in lines]
        for atom in atoms:
            elem = atom[0]
            coords = list(map(float, atom[1:4]))
            if elem in position:
                position[elem].append(coords)
            else:
                position[elem] = [coords]
    return position


atom_masses = {'Cu': 63.546, 'Ni': 58.693}  # 用于质心坐标计算的原子质量字典，根据需求添加原子质量


def get_mass_center(position: dict, atom_mass: dict) -> np.ndarray:
    numerator = []
    denominator = 0.0

    for atom, pos_list in position.items():
        coords = np.array(pos_list, dtype=float)  # shape: (n_atoms, 3)
        mass = atom_mass[atom]
        n = len(pos_list)

        weighted_sum = mass * np.sum(coords, axis=0)  # 向量
        numerator.append(weighted_sum)
        denominator += mass * n

    center_of_mass = np.sum(numerator, axis=0) / denominator
    return center_of_mass


def atom_analyse(position: dict, center: np.ndarray, elem: str, cut: float) -> str:
    surface_num = 0
    inner_num = 0
    for pos in position[elem]:
        np_pos = np.array(pos, dtype=float)
        distance = np.linalg.norm(np_pos - center)
        if distance > cut:
            surface_num += 1
        else:
            inner_num += 1

    return f"number of surface {element} atoms is {surface_num},number of inner {element} atoms is {inner_num}"


structure = read('5ns.xyz')
ase_test = structure.get_center_of_mass()
print(ase_test)
atom_position = read_position("5ns.xyz")
center_vector = get_mass_center(atom_position, atom_masses)
print(center_vector)
cutoff = 9  # 设置截断半径，与质心之间的距离，从而判断是否是表面原子
element = "Cu"
result = atom_analyse(atom_position, center_vector, element, cutoff)

print(result)
