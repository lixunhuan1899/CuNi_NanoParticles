#!/bin/bash
#对随机生成的纯的Cu Nano particles进行升温退火md模拟，以期得到较为规则的晶体结构

mkdir -p trajs
mkdir -p logs

T_Cu=1357.77

#annel
echo "start annel process"

start_anneal=$(date +%s)

cat > input <<EOF
atoms_file = 'Cu.xyz'
pot_file = 'gap_files/CuNi.gap'

n_species = 1
species = Cu
masses  = 63.546
e0 = -0.21472241

md_nsteps = 5000
md_step = 4.

optimize = "vv"
thermostat = "bussi"
t_beg = ${T_Cu}
t_end = ${T_Cu}
tau_t = 10.
EOF

mpirun -np 64 turbogap md &>  /dev/null 

#从trajectory_out.xyz中提取原子的个数
n=$(head -n 1 trajectory_out.xyz | awk '{print $1+2}')
tail -n "$n" trajectory_out.xyz > atoms.xyz
mv thermo.log logs/annel_Cu.log

end_anneal=$(date +%s)
echo "annel process finished, time used: $((end_anneal-start_anneal)) seconds"


#Quench

echo "start quench process"
start_quench=$(date +%s)

cat >input<<EOF
atoms_file = 'atoms.xyz'
pot_file = 'gap_files/CuNi.gap'

n_species = 1
species = Cu
masses  = 63.546
e0 = -0.21472241

md_nsteps = 5000
md_step = 4.

optimize = "vv"
thermostat = "bussi"
t_beg = ${T_Cu}
t_end = 100.
tau_t = 100.

write_xyz = 250
EOF

mpirun -np 64 turbogap md &>  /dev/null 

n=$(head -n 1 trajectory_out.xyz | awk '{print $1+2}')
tail -n "$n" trajectory_out.xyz > atoms.xyz
mv trajectory_out.xyz trajs/Cu_quench.xyz
mv thermo.log logs/quench_Cu.log

end_quench=$(date +%s)
echo "quench process finished, time used: $((end_quench-start_quench)) seconds"

#Relax
echo "start relax process"
start_relax=$(date +%s) 

cat > input <<EOF
atoms_file = 'atoms.xyz'
pot_file = 'gap_files/CuNi.gap'

n_species = 1
species = Cu
masses  = 63.546
e0 = -0.21472241

md_nsteps = 5000

optimize = "gd"
EOF

mpirun -np 64 turbogap md &>  /dev/null 

n=$(head -n 1 trajectory_out.xyz | awk '{print $1+2}')
tail -n "$n" trajectory_out.xyz > trajs/Cu_relax.xyz
mv thermo.log logs/relax_Cu.log
rm trajectory_out.xyz
rm input

end_relax=$(date +%s)
echo "relax process finished, time used: $((end_relax-start_relax)) seconds"


