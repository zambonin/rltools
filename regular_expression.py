#!/usr/bin/env python
# -*- coding: utf-8 -*-
from automaton import Automaton
from pprint import pprint

class RegularExpression:
    def __init__(self, expression, alphabet):
        self.expression = expression
        self.alphabet = alphabet
        self.list = []
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
            aux[frozenset(["q1"+transition])] = {}
            automaton.transitions = aux
            return self.renaming_automaton(automaton, "%")

        def empty_word(self):
            automaton = Automaton(set(),set(),{},"",set())
            automaton.init_state = "q0"
            automaton.states.add("q0")
            automaton.final_states.add("q0")
            aux = {}
            automaton.transitions = aux
            return automaton

        def concatenation(self, automatons):
            automaton = Automaton(set(),set(),{},"",set())
            automaton1 = self.renaming_automaton(automatons[0], "#")
            automaton2 = self.renaming_automaton(automatons[1], "$")

            automaton.init_state = automaton1.init_state
            automaton.final_states = automaton2.final_states
            automaton.alphabet.update(automaton1.alphabet | automaton2.alphabet)
            automaton.states.update(automaton1.states | automaton2.states)
            automaton.transitions.update(automaton1.transitions)
            automaton.transitions.update(automaton2.transitions)
            for state in automaton1.final_states:
                try:
                    automaton.transitions[state][automaton.epsilon].add(automaton2.initial_state)
                except KeyError:
                    automaton.transitions[state][automaton.epsilon] = set()
                    automaton.transitions[state][automaton.epsilon].add(automaton2.initial_state)



            """automaton = Automaton(set(),set(),{},"",set())
            automatons = automatons
            aux_int = 0
            last_state = []
            for aux_autom in automatons:
                automaton.alphabet.update(aux_autom.alphabet)
                if aux_int == 0:
                    automaton.init_state = (aux_autom.init_state)+"_"+str(aux_int)
                for state in aux_autom.states:
                    automaton.states.add(state+"_"+str(aux_int))
                    automaton.transitions[frozenset([state+"_"+str(aux_int)])] = {}
                    if frozenset([state]) in aux_autom.transitions and state not in aux_autom.final_states:
                        for step in aux_autom.transitions[frozenset([state])]:
                            next = set(aux_autom.transitions[frozenset([state])][step].pop())
                            actual = frozenset([state+"_"+str(aux_int)])
                            automaton.transitions[actual][step] = {}
                            automaton.transitions[actual][step] = {frozenset([next.pop()+"_"+str(aux_int)])}
                            if aux_int != 0:
                                lst_state = last_state.pop(0)
                                automaton.final_states.remove(lst_state)
                                automaton.transitions[frozenset([lst_state])][automaton.epsilon] = {frozenset([state+"_"+str(aux_int)])}
                    else:
                        automaton.final_states.add(state+"_"+str(aux_int))
                        last_state.append(state+"_"+str(aux_int))
                aux_int+=1
            return self.fix_automaton(automaton)"""

        def or_operation(self, automatons):
            automaton = Automaton(set(),set(),{},"",set())
            automatons = automatons
            automaton.init_state = "initialOr"
            automaton.states.add("initialOr")
            automaton.transitions[frozenset(["initialOr"])] = {}
            automaton.transitions[frozenset(["initialOr"])][automaton.epsilon] = set()
            for automaton_aux in automatons:
                automaton.alphabet.add(automaton_aux.alphabet.pop())
                automaton.states.update(automaton_aux.states)
                automaton.transitions.update(automaton_aux.transitions)
                automaton.final_states.update(automaton_aux.final_states)
                automaton.transitions[frozenset(["initialOr"])][automaton.epsilon].add(automaton_aux.init_state)
            return self.fix_automaton(automaton)

        def closure(self, automatons):
            automaton = Automaton(set(),set(),{},"",set())
            automatons = automatons
            automaton.init_state = "initialClosure"
            automaton.states.add("initialClosure")
            automaton.final_states.add("initialClosure")
            automaton.transitions[frozenset(["initialClosure"])] = {}
            automaton.transitions[frozenset(["initialClosure"])][automaton.epsilon] = set()
            for automaton_aux in automatons:
                automaton.alphabet.add(automaton_aux.alphabet.pop())
                automaton.states.update(automaton_aux.states)
                automaton.final_states.update(automaton_aux.final_states)
                automaton.transitions[frozenset(["initialClosure"])][automaton.epsilon].add(automaton_aux.init_state)
                automaton.transitions.update(automaton_aux.transitions)
                for state in automaton_aux.final_states:
                    automaton.transitions[frozenset([state])][automaton.epsilon] = set()
                    automaton.transitions[frozenset([state])][automaton.epsilon].add(frozenset(["initialClosure"]))
            return self.fix_automaton(automaton)

        def execute_operations(self):
            automatons = []
            while len(self.list) != 0:
                caracter = self.list.pop(0)
                if caracter in self.alphabet:
                    if len(automatons) == 2 and self.list[0] in self.alphabet:
                        automatons_aux = [automatons.pop()]
                        automatons_aux.append(single_state(self, caracter))
                        automatons.append(concatenation(self, automatons_aux))
                    else:
                        automatons.append(single_state(self, caracter))
                if caracter == "|":
                    if len(automatons) > 2 and len(automatons) == 3:
                        automatons_aux = [automatons.pop(1)]
                        automatons_aux.append(automatons.pop())
                        automatons.append(concatenation(self, automatons_aux))
                    automatons = [or_operation(self, automatons)]
                #if caracter == "*":
                    #aut = [automatons.pop()]
                    #automatons.append(closure(self, aut))

            if len(automatons) == 2:
                return concatenation(self, automatons)
            else:
                return automatons.pop()

        def analyse_expression(self, expression):
            expression = expression
            i = 0
            while len(expression) != 0:
                if expression[i] in self.alphabet:
                    self.list.append(expression[i])
                    expression = expression[:i] + expression[i+1:]
                elif expression[i] == "|":
                    next = expression[i+1]
                    if next == "(":
                        aux = 2
                        while next != ")":
                            next = expression[i+aux]
                            if next != ")":
                                self.list.append(next)
                            aux+=1
                        expression = expression[:i] + expression[i+aux:]
                    else:
                        self.list.append(next)
                        expression = expression[:i] + expression[i+2:]
                    self.list.append("|")
                elif expression[i] == "(" or expression[i] == ")":
                    expression = expression[:i] + expression[i+1:]
                elif expression[i] == "*":
                    self.list.append("*")
                    expression = expression[:i] + expression[i+1:]

        analyse_expression(self, self.expression)
        return execute_operations(self)

    def renaming_automaton(self, automaton, sufix):
            automaton_aux = Automaton(set(),set(),{},"",set())
            automaton_aux.alphabet.update(automaton.alphabet)
            automaton_aux.init_state = automaton.init_state+sufix
            for state in automaton.final_states:
                automaton_aux.final_states.add(frozenset([set([state]).pop()+sufix]))
            for state in automaton.states:
                automaton_aux.states.add(state+sufix)
            for state in automaton.transitions:
                automaton_aux.transitions[frozenset([set(state).pop()+sufix])] = {}
                for symbol in automaton.transitions[state]:
                    automaton_aux.transitions[frozenset([set(state).pop()+sufix])][symbol] = set()
                    for element in automaton.transitions[state][symbol]:
                        automaton_aux.transitions[frozenset([set(state).pop()+sufix])][symbol].add(frozenset([set(element).pop()+sufix]))
            return automaton_aux

    def fix_automaton(self, automaton):
        for letter in automaton.alphabet:
            for state in automaton.transitions:
                try:
                    automaton.transitions[state][letter]
                except KeyError:
                    automaton.transitions[state][letter] = {}
                    automaton.transitions[state][letter] = set()
        return automaton



def test():
    a = RegularExpression("(((a|b)*)|(bbb*))*", {"a","b"})
    aux = a.regular_to_automaton()
    pprint(aux.transitions)
    print("final:",aux.final_states)
    print("init:",aux.init_state)
    print("states:",aux.states)

test()