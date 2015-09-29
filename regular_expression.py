#!/usr/bin/env python
# -*- coding: utf-8 -*-
from automaton import Automaton
from pprint import pprint

class RegularExpression:
    def __init__(self, expression, alphabet):
        self.expression = expression
        self.alphabet = alphabet
        self.empty_word = "ε"

    def regular_to_automaton(self):
        def single_state(self, transition):
            automaton = Automaton(set(),set(),{},"",set())
            automaton.init_state = "q0"+transition
            automaton.alphabet.add(transition)
            automaton.states.add("q0"+transition)
            automaton.states.add("q1"+transition)
            automaton.final_states.add("q1"+transition)
            aux = {}
            aux[frozenset(["q0"+transition])] = {}
            aux[frozenset(["q0"+transition])][transition] = {frozenset(["q1"+transition])}
            automaton.transitions = aux
            return automaton

        def empty_word(self):
            automaton = Automaton(set(),set(),{},"",set())
            automaton.init_state = "q0"
            automaton.states.add("q0")
            automaton.final_states.add("q0")
            aux = {}
            automaton.transitions = aux
            return automaton

        def concatenation(self, transition):
            automaton = Automaton(set(),set(),{},"",set())
            automaton.init_state = "q0"
            auxd = {}
            aux = 0
            for letter in transition:
                automaton.alphabet.add(letter)
                automaton.states.add("q"+str(aux)+letter)
                auxd[frozenset(["q"+str(aux)+letter])] = {}
                auxd[frozenset(["q"+str(aux)+letter])][letter] ={frozenset(["q"+str((aux+1))+letter])}
                ++aux
            automaton.final_states.add("q"+str(len(letter))+letter[len(letter)-1])
            automaton.transitions = auxd
            return automaton

        if len(self.expression) == 2:
            return concatenation(self, self.expression)
def test():
    a = RegularExpression("ab", {"a","b"})
    aux = a.regular_to_automaton()
    pprint(aux.transitions)
    print("final:",aux.final_states)
    print("init:",aux.init_state)
    print("states:",aux.states)

test()