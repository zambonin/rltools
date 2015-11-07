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
            actual_state = frozenset([self.automaton.init_state])
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

    a = Tokenizer(b, "pasqual.pac")
    a.analyze()


test()
