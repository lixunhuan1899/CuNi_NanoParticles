#!/bin/bash
#对随机生成的纯的Cu Nano particles进行升温退火md模拟，以期得到较为规则的晶体结构

system="CuNi"

mkdir -p trajs
mkdir -p logs



T=1550
anneal_T=1400

#melt
echo "start melt process"

start_melt=$(date +%s)

cat > input <<EOF
atoms_file = 'CuNi_480.xyz'
pot_file = 'gap_files/CuNi.gap'

n_species = 2
species = Cu Ni
masses = 63.546 58.693
e0 = -0.21472241 -1.59815363

md_nsteps = 100000
md_step = 1.

optimize = "vv"
thermostat = "bussi"
t_beg = ${T}
t_end = ${T}
tau_t = 10.
EOF

mpirun -np 96 turbogap md &>  /dev/null 

#从trajectory_out.xyz中提取原子的个数
n=$(head -1 trajectory_out.xyz | awk '{print $1+2}')
tail -$n trajectory_out.xyz > atoms_melt.xyz
mv thermo.log logs/melt_CuNi.log

end_melt=$(date +%s)
echo "melt process finished, time used: $((end_melt-start_melt)) seconds"


#anneal

echo "start anneal process"

start_anneal=$(date +%s)

cat > input <<EOF
atoms_file = 'atoms_melt.xyz'
pot_file = 'gap_files/CuNi.gap'

n_species = 2
species = Cu Ni
masses = 63.546 58.693
e0 = -0.21472241 -1.59815363

md_nsteps = 1000000
md_step = 1.

optimize = "vv"
thermostat = "bussi"
t_beg = ${anneal_T}
t_end = ${anneal_T}
tau_t = 10.
EOF

mpirun -np 96 turbogap md &>  /dev/null 

#从trajectory_out.xyz中提取原子的个数
n=$(head -1 trajectory_out.xyz | awk '{print $1+2}')
tail -$n trajectory_out.xyz > atoms_anneal.xyz
mv thermo.log logs/anneal_CuNi.log

end_anneal=$(date +%s)
echo "anneal process finished, time used: $((end_anneal-start_anneal)) seconds"


#Quench

echo "start quench process"
start_quench=$(date +%s)

cat >input<<EOF
atoms_file = 'atoms_anneal.xyz'
pot_file = 'gap_files/CuNi.gap'

n_species = 2
species = Cu Ni
masses = 63.546 58.693
e0 = -0.21472241 -1.59815363

md_nsteps = 1000000
md_step = 1.

optimize = "vv"
thermostat = "bussi"
t_beg = ${annneal_T}
t_end = 300.
tau_t = 100.

write_xyz = 250
EOF

mpirun -np 96 turbogap md &>  /dev/null 

n=$(head -1 trajectory_out.xyz | awk '{print $1+2}')
tail -$n trajectory_out.xyz > atoms_quench.xyz
mv trajectory_out.xyz trajs/CuNi_quench.xyz
mv thermo.log logs/quench_CuNi.log

end_quench=$(date +%s)
echo "quench process finished, time used: $((end_quench-start_quench)) seconds"

#Relax
echo "start relax process"
start_relax=$(date +%s) 

cat > input <<EOF
atoms_file = 'atoms_quench.xyz'
pot_file = 'gap_files/CuNi.gap'

n_species = 2
species = Cu Ni
masses = 63.546 58.693
e0 = -0.21472241 -1.59815363

md_nsteps = 50000

optimize = "gd"
EOF

mpirun -np 96 turbogap md &>  /dev/null 

n=$(head -1 trajectory_out.xyz | awk '{print $1+2}')
tail -$n trajectory_out.xyz > trajs/CuNi_relax.xyz
mv thermo.log logs/relax_CuNi.log
rm trajectory_out.xyz
rm input

end_relax=$(date +%s)
echo "relax process finished, time used: $((end_relax-start_relax)) seconds"








