import sys
import os
i=0.2
def read_xyz(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    num_atoms = int(lines[0].strip())
    #comment = lines[1].strip()
    comment = "CuNi_Cluster"
    atoms = [line.split() for line in lines[2:num_atoms+2]]
    return num_atoms, comment, atoms

def write_poscar(output_path, num_atoms, comment, atoms):
    element_counts = {}
    element_positions = {}
    
    for atom in atoms:
        element = atom[0]
        if element in element_counts:
            element_counts[element] += 1
            element_positions[element].append(atom[1:4])
        else:
            element_counts[element] = 1
            element_positions[element] = [atom[1:4]]
    
    with open(output_path, 'w') as f:
        f.write(f"{comment}\n")
        f.write("1.0\n")  # 缩放因子
        f.write("31.764 0.0 0.0\n0.0 31.952.0 0.0\n0.0 0.0 32.354\n")  # 假设为立方体
        
        elements = sorted(element_counts.keys())  # 保证元素按照字母顺序排列
        f.write(" ".join(elements) + "\n")
        f.write(" ".join(str(element_counts[el]) for el in elements) + "\n")
        f.write("Cartesian\n")
        
        for element in elements:  # 先输出所有Cu的坐标，再输出所有Ni的坐标
            for pos in element_positions[element]:
                f.write(f"{pos[0]} {pos[1]} {pos[2]}\n")

def xyz_to_poscar(xyz_path, poscar_path):
    num_atoms, comment, atoms = read_xyz(xyz_path)
    write_poscar(poscar_path, num_atoms, comment, atoms)
    print(f"Conversion complete: {poscar_path}")
    
poscar_dir = "./0.2"  
poscar_file = os.path.join(poscar_dir, "POSCAR")
os.makedirs(poscar_dir, exist_ok=True)
xyz_file = "./0.2.xyz"
poscar_file = f"./{i}/POSCAR"
xyz_to_poscar(xyz_file, poscar_file)


