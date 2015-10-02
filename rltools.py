#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""rltools.py

The command-line interface for this program.

Gustavo Zambonin & Matheus Ben-Hur de Melo Leite, UFSC, October 2015.
"""

import re
import sys
from algorithms.io_manager import load, save
from algorithms.finite_automaton import FiniteAutomaton
from algorithms.regular_grammar import RegularGrammar
from algorithms.regular_expression import RegularExpression

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Basic usage: man ./rltools")

    possible_commands = ["--dfa", "--gta", "--atg", "--rta", "--atr"]

    if len(set(sys.argv).intersection(possible_commands)) > 1:
        print("Only one flag is permitted at a time.")

    if sys.argv[1] not in possible_commands:
        print("Invalid command.")

    if len(sys.argv) > 2:
        if "--dfa" in sys.argv:
            aut = load(sys.argv[2])
            if type(aut) is FiniteAutomaton:
                aut.determinize()
                outpath = re.sub('.in', r'.out', sys.argv[2])
                if '/' in outpath:
                    savepath = re.sub('/', r'/afd-', outpath)
                else:
                    savepath = 'afd-' + outpath
                save(savepath, 'automaton', aut)
                print("DFA saved in %s!" % savepath)
            else:
                print("Input must be an automaton.")

        elif "--gta" in sys.argv:
            grm = load(sys.argv[2])
            if type(grm) is RegularGrammar:
                aut = RegularGrammar.grammar_to_automaton(grm)
                outpath = re.sub('.in', r'.out', sys.argv[2])
                if '/' in outpath:
                    savepath = re.sub('/', r'/afd-', outpath)
                else:
                    savepath = 'afd-' + outpath
                save(savepath, 'automaton', aut)
                print("DFA saved in %s!" % savepath)
            else:
                print("Input must be a grammar.")

        elif "--atg" in sys.argv:
            aut = load(sys.argv[2])
            if type(aut) is FiniteAutomaton:
                grm = RegularGrammar.automaton_to_grammar(aut)
                outpath = re.sub('.in', r'.out', sys.argv[2])
                if '/' in outpath:
                    savepath = re.sub('/', r'/gr-', outpath)
                else:
                    savepath = 'gr-' + outpath
                save(savepath, 'grammar', grm)
                print("GR saved in %s!" % savepath)
            else:
                print("Input must be an automaton.")

        elif "--rta" in sys.argv:
            reg = sys.argv[2]
            if type(reg) is str:
                regexp = RegularExpression(reg)
                aut = RegularExpression.regexp_to_automaton(regexp)
                savepath = "tests/afnd-reg.out"
                save(savepath, 'automaton', aut)
                print("DFA saved in %s!" % savepath)
            else:
                print("Input must be a regular expression.")

        elif "--atr" in sys.argv:
            aut = load(sys.argv[2])
            if type(aut) is FiniteAutomaton:
                reg = RegularExpression.automaton_to_regexp(aut)
                outpath = re.sub(r'.in', r'.out', sys.argv[2])
                if '/' in outpath:
                    savepath = re.sub('/', r'/re-', outpath)
                else:
                    savepath = 're-' + outpath
                save(savepath, 'regexp', reg)
                print("RE saved in %s!" % savepath)
            else:
                print("Input must be an automaton.")

    else:
        print("Input file is missing.")
