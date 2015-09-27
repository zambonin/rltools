#!/usr/bin/bash

automata=$1

../rltools.py --dfa $automata.in
../rltools.py --atg afd-$automata.out
../rltools.py --gta gr-afd-$automata.out
../rltools.py --atg afd-gr-afd-$automata.out

if [ $(wc -l < afd-$automata.out) -eq $(wc -l < afd-gr-afd-$automata.out) ]; then
    echo "automata pair is equal"
fi

if [ $(wc -l < gr-afd-$automata.out) -eq $(wc -l < gr-afd-gr-afd-$automata.out) ]; then
    echo "grammar pair is equal"
fi
