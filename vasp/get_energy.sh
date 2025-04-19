#!/bin/bash

for i in $(seq 1 9);do

    cd vasp_ST_$i
    
    while read -r line; do
    
         if [[ $line == DAV:* ]]; then
             dav_step=$(echo "$line" | awk '{print $2}')
            if (( dav_step >= 200 )); then
               echo "structure$i is not convergence! DAV steps: $dav_step"
               exit 1
            fi
         fi
    done  < OSZICAR
    
    echo "structure$i is convergence! start get energy..."
    grep "E0" OSZICAR | sed -n 's/.*E0= *\(-[0-9.E+-]*\).*/\1/p' >> ../energy.dat
    
    cd ..
    
done
    
    
    
