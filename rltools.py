#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from algorithms.io_manager import *

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Basic usage: man ./rltools")

    possible_commands = ["--dfa", "--gta", "--atg"]

    if len(set(sys.argv).intersection(possible_commands)) > 1:
        print("Only one flag is permitted at a time.")

    if sys.argv[1] not in possible_commands:
        print("Invalid command.")

    if len(sys.argv) > 2:
        if "--dfa" in sys.argv:
            aut = load(sys.argv[2])
            if type(aut) is FiniteAutomaton:
                aut.determinize()
                savepath = 'afd-' + re.sub('.in', r'.out', sys.argv[2])
                save(savepath, 'automaton', aut)
                print("DFA saved in %s!" % savepath)
            else:
                print("Input must be an automaton.")

        elif "--gta" in sys.argv:
            grm = load(sys.argv[2])
            if type(grm) is RegularGrammar:
                aut = RegularGrammar.grammar_to_automaton(grm)
                savepath = 'afd-' + re.sub('.in', r'.out', sys.argv[2])
                save(savepath, 'automaton', aut)
                print("DFA saved in %s!" % savepath)
            else:
                print("Input must be a grammar.")

        elif "--atg" in sys.argv:
            aut = load(sys.argv[2])
            if type(aut) is FiniteAutomaton:
                grm = RegularGrammar.automaton_to_grammar(aut)
                savepath = 'gr-' + re.sub('.in', r'.out', sys.argv[2])
                save(savepath, 'grammar', grm)
                print("GR saved in %s!" % savepath)
            else:
                print("Input must be an automaton.")

    else:
        print("Input file is missing.")
