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
                curr_state, word = frozenset([self.automaton.init_state]), ""
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
    b.states.add("q0")
    b.states.add("q1")
    b.states.add("q2")
    b.states.add("q3")
    b.states.add("q4")

    b.init_state = "q0"
    b.final_states.add(frozenset(["q4"]))

    b.transitions[frozenset(["q0"])] = {}
    b.transitions[frozenset(["q0"])]["e"] = {"q1"}
    b.transitions[frozenset(["q0"])]["l"] = set()
    b.transitions[frozenset(["q0"])]["s"] = set()

    b.transitions[frozenset(["q1"])] = {}
    b.transitions[frozenset(["q1"])]["e"] = set()
    b.transitions[frozenset(["q1"])]["l"] = {"q2"}
    b.transitions[frozenset(["q1"])]["s"] = set()

    b.transitions[frozenset(["q2"])] = {}
    b.transitions[frozenset(["q2"])]["e"] = set()
    b.transitions[frozenset(["q2"])]["l"] = set()
    b.transitions[frozenset(["q2"])]["s"] = {"q3"}

    b.transitions[frozenset(["q3"])] = {}
    b.transitions[frozenset(["q3"])]["e"] = {"q4"}
    b.transitions[frozenset(["q3"])]["l"] = set()
    b.transitions[frozenset(["q3"])]["s"] = set()

    b.transitions[frozenset(["q4"])] = {}
    b.transitions[frozenset(["q4"])]["e"] = set()
    b.transitions[frozenset(["q4"])]["l"] = set()
    b.transitions[frozenset(["q4"])]["s"] = set()

    b.alphabet.add("e")
    b.alphabet.add("l")
    b.alphabet.add("s")

    b = Tokenizer(b, "pasqual.pac")
    b.analyze()

test()
