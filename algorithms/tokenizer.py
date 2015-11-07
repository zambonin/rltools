#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tokenizer.py

A simple text segmentation utility for the lexical analysis part of a compiler.

Gustavo Zambonin & Matheus Ben-Hur de Melo Leite, UFSC, November 2015.
"""

from finite_automaton import FiniteAutomaton
from pprint import pprint


class Tokenizer(object):
    """A tokenizer performs lexical analysis by going through every character
    of an input string (the source code desired to be proof-read) and matching
    it with words accepted by a finite automaton.

    Attributes:
        automaton: the means by which the words are computed.
        input_file: a text file with source code for the language.
    """
    def __init__(self, automaton, input_file):
        """Inits Tokenizer with the attributes introduced above."""
        self.automaton = automaton
        self.input_file = input_file

    def analyze(self):
        """Reads lexemes from a file and transforms them in tokens."""
        with open(self.input_file, 'r') as file:
            tokens, errors, separators = [], [], ["\n", " "]
            line_number = 0
            while True:
                line = file.readline()
                if not line:
                    break
                line_number += 1
                curr_state, word = frozenset(self.automaton.init_state), ""
                for letter in line:
                    if ((curr_state == frozenset() or curr_state == set())
                       and letter not in separators):
                        word += str(letter)
                    elif letter in separators:
                        if curr_state in self.automaton.final_states:
                            aux = "".join(p for p in set(curr_state))
                            tokens.append((word, aux))
                        else:
                            errors.append("{}:{} '{}' not recognized".format(
                                          self.input_file, line_number, word))
                        curr_state = frozenset(self.automaton.init_state)
                        word = ""
                    else:
                        word += str(letter)
                        try:
                            curr_state = frozenset(
                                self.automaton.transitions[curr_state][letter])
                        except KeyError:
                            curr_state = set()

        print('Tokens')
        pprint([t for t in tokens])
        print('\nErrors')
        pprint([e for e in errors])


def test():
    b = FiniteAutomaton(set(), set(), {}, "0", set())
    b.states.add("S")
    b.states.add("A")
    b.states.add("B")
    b.states.add("C")

    b.init_state = "S"
    b.final_states.add(frozenset(["C"]))

    b.transitions[frozenset(["S"])] = {}
    b.transitions[frozenset(["S"])]["a"] = {"A"}
    b.transitions[frozenset(["S"])]["b"] = set()

    b.transitions[frozenset(["A"])] = {}
    b.transitions[frozenset(["A"])]["a"] = set()
    b.transitions[frozenset(["A"])]["b"] = {"B"}

    b.transitions[frozenset(["B"])] = {}
    b.transitions[frozenset(["B"])]["a"] = {"C"}
    b.transitions[frozenset(["B"])]["b"] = {"B"}

    b.transitions[frozenset(["C"])] = {}
    b.transitions[frozenset(["C"])]["a"] = set()
    b.transitions[frozenset(["C"])]["b"] = set()

    b.alphabet.add("a")
    b.alphabet.add("b")

    a = Tokenizer(b, "pasqual.pac")
    a.analyze()

test()
