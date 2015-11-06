#!/usr/bin/env python
# -*- coding: utf-8 -*-

from finite_automaton import FiniteAutomaton


class Tokenizer(object):
    def __init__(self, automaton, input_file):
        self.automaton = automaton
        self.input_file = input_file
        self.tokens = list()
        self.errors = list()

    def analyze(self):
        file = open(self.input_file, 'r')
        line_number = 0
        while True:
            line = file.readline()
            if not line: break
            line_number += 1
            words = line
            actual_state = frozenset(self.automaton.init_state)
            word = ""
            for letter in words:
                if (actual_state == frozenset() or actual_state == set()) and letter != "\n":
                    word += str(letter)
                else:
                    if letter == " " or letter == "\n":
                        if actual_state in self.automaton.final_states:
                            aux = ""
                            for piece in set(actual_state):
                                aux += piece
                                self.tokens.append((word, aux))
                            actual_state = frozenset(self.automaton.init_state)
                            word = ""
                        else:
                            self.errors.append("ERROR: The word " + word + " in line " + str(line_number) + " cannot be recognized")
                            actual_state = frozenset(self.automaton.init_state)
                            word = ""
                    else:
                        word += str(letter)
                        try:
                            actual_state = frozenset(self.automaton.transitions[actual_state][letter])
                        except KeyError:
                            actual_state = set()

        file.close()
        print("Tokens", self.tokens)
        print("Errors", self.errors)


def test():
    b = FiniteAutomaton(set(), set(), {}, "0", set())
    b.states.add("S")
    b.states.add("A")
    b.states.add("B")
    b.states.add("C")
    b.states.add("D")

    b.init_state = "S"
    b.final_states.add(frozenset(["C"]))
    b.final_states.add(frozenset(["D"]))

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
    b.transitions[frozenset(["C"])]["a"] = {"D"}
    b.transitions[frozenset(["C"])]["b"] = set()

    b.transitions[frozenset(["D"])] = {}
    b.transitions[frozenset(["D"])]["a"] = set()
    b.transitions[frozenset(["D"])]["b"] = set()

    b.alphabet.add("a")
    b.alphabet.add("b")

    a = Tokenizer(b, "pasqual.pac")
    a.analyze()


test()
