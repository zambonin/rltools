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
            automatons = []
            transitions={}
            aux_int = 0
            last_state = []
            for letter in transition:
                automatons.append(single_state(self,letter))
                aux_autom = automatons.pop()
                automaton.alphabet.add(letter)
                if aux_int == 0:
                    automaton.init_state = (aux_autom.init_state)+str(aux_int)
                for state in aux_autom.states:
                    automaton.states.add(state+str(aux_int))
                    automaton.transitions[frozenset([state+str(aux_int)])] = {}
                    if frozenset([state]) in aux_autom.transitions:
                        for step in aux_autom.transitions[frozenset([state])]:
                            next = set(aux_autom.transitions[frozenset([state])][step].pop())
                            actual = frozenset([state+str(aux_int)])
                            automaton.transitions[actual][step] = {}
                            automaton.transitions[actual][step] = {frozenset([next.pop()+str(aux_int)])}
                            if aux_int != 0:
                                lst_state = last_state.pop(0)
                                automaton.final_states.remove(lst_state)
                                automaton.transitions[frozenset([lst_state])][automaton.epsilon] = {frozenset([state+str(aux_int)])}
                    else:
                        automaton.final_states.add(state+str(aux_int))
                        last_state.append(state+str(aux_int))
                aux_int+=1



            return automaton

        if len(self.expression) == 3:
            return concatenation(self, self.expression)
def test():
    a = RegularExpression("abc", {"a","b","c"})
    aux = a.regular_to_automaton()
    pprint(aux.transitions)
    print("final:",aux.final_states)
    print("init:",aux.init_state)
    print("states:",aux.states)

test()