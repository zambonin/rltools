#!/usr/bin/bash

# builder.sh
# Gustavo Zambonin & Matheus Ben-Hur de Melo Leite, UFSC, November 2015.

# Usage:
# sh builder.sh

keyword='else|if|while|read|write|int([])*|bool|str|False|True'
letter=$(echo {a..z} {A..Z})
digit=$(echo {0..9})
nonzerodigit=$(echo {1..9})
identifier="((${letter// /|})(${letter// /|}|${digit// /|}|_)*)"
integer="(((${nonzerodigit// /|})(${digit// /|})*)|0)"
char=$(sed 's/["()*\|]//g; s/./&|/g' <<< \
       "$(awk 'BEGIN{for(i=32;i<127;i++)printf "%c",i}'; echo)")
string="(\"(${char%?})*\")"

cd ..
./rltools.py --rta "$keyword|$identifier|$integer|$string" >/dev/null
cd tests && mv afnd-reg.out master-automaton.out
echo "Automaton saved in tests/master-automaton.out!"
