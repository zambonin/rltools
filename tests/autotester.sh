#!/usr/bin/bash

# autotester.sh
# Gustavo Zambonin & Matheus Ben-Hur de Melo Leite, UFSC, October 2015.

# Usage:
# sh autotester.sh <NFA file>

if [[ $1 ]]; then
    IFS='.' read -r filename ext <<< "$1"
    ../rltools.py --dfa $filename.$ext
    ../rltools.py --atg afd-$filename.out

    if [[ ! $(echo "$filename" | grep reg) ]]; then
        ../rltools.py --gta gr-afd-$filename.out
        ../rltools.py --atg afd-gr-afd-$filename.out

        if [ $(wc -l < afd-$filename.out) -eq \
             $(wc -l < afd-gr-afd-$filename.out) ]; then
            echo "automata pair is equal!"
        fi

        if [ $(wc -l < gr-afd-$filename.out) -eq \
             $(wc -l < gr-afd-gr-afd-$filename.out) ]; then
            echo "grammar pair is equal!"
        fi
    fi
else
    echo "arg is missing"
fi
