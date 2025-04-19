#!/bin/bash

for i in $(seq 1 5); do

    mkdir vasp_ST_${i}
    cd  vasp_ST_${i}
    
    cp ../INCAR ../POTCAR ../KPOINTS .
    
    cp ../POSCAR/POSCAR_${i} POSACR 
    
    n_Ni=$(awk 'NR==7 {print $2}' "POSCAR")
    
    n_others=$((50 - n_Ni))
    magmom_values=$(printf "2.5 %.0s" $(seq 1 "$n_Ni")) 
    if [[ ${n_others} -eq 0 ]];then 
    magmom_line="$magmom_values"
    else
    magmom_line="$n_others*0.0 $magmom_values"
    fi
    
    if grep -q "^MAGMOM" "INCAR"; then
       sed -i "s/^MAGMOM.*/MAGMOM = $magmom_line/" "INCAR"
    else
       echo "MAGMOM = $magmom_line" >> "$incar_file"
    fi

    echo "MAGMOM updated in $incar_file:"
    echo "MAGMOM = $magmom_line"
   
    mpirun -np 28 vasp_gam
    
    
    cd ..
    
done
