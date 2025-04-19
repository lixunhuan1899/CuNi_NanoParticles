#!/bin/bash

mkdir -p trajs/
mkdir -p logs/

for i in  $(seq 1 1 5); do

SECONDS=0
echo "Doing ${i}/5 ..."

cat>input<<EOF
atoms_file="init_xyz/init_xyz/${i}.xyz"
pot_file="gap_files/CuNi.gap"

species=Cu Ni
n_species=2
EOF

mpirun -np turbogap predict
trajectory_out.xyz>> trajs/${i}.xyz
mv thermo.log logs/${i}.log
rm trajectory_out.xyz
rm input

echo "... in ${SECONDS} s"

done 
