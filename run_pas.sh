#!/bin/sh
for f in $2/*; do
    if [[ $f == *"pa"* ]]; then
        echo $f
        python find_aas.py $1 $f
    fi
done
