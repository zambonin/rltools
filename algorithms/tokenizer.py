#!/usr/bin/env python
# -*- coding: utf-8 -*-

from finite_automaton import FiniteAutomaton

class Tokenizer(object):

    def __init__(self, automaton, input_file):
        self.automaton = automaton
        self.input_file = input_file
        self.tokens = list()
        self.errors = list()


    def analyse(self):
        file = open(self.input_file, 'r')
        line_number = 0
        while True:
            line = file.readline()
            if not line: break
            line_number += 1
            words = line.split(" ")
            for word in words:
                if word != "":
                    actual_state = frozenset(self.automaton.init_state)
                    for letter in word:
                        if actual_state == frozenset() or set() or letter == "\n":
                            break
                        try:
                            actual_state = frozenset(self.automaton.transitions[actual_state][letter])
                        except KeyError:
                            actual_state = set()
                    if actual_state in self.automaton.final_states:
                        self.tokens.append((word, actual_state))
                    else:
                        self.errors.append("ERROR: The word "+word+" in line "+str(line_number)+" cannot be recognized")

        print(self.tokens)
        print(self.errors)





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
    a.analyse()

test()