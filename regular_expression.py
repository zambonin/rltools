#!/usr/bin/env python
# -*- coding: utf-8 -*-

from automaton import Automaton
from pprint import pprint

class RegularExpression:
    def __init__(self, expression):
        self.expression = expression
        valid_symbols = list(map(chr, range(65, 91))) + \
                        list(map(chr, range(97, 123))) + \
                        [str(i) for i in range(10)]
        self.alphabet = {i for i in expression if i in valid_symbols}
        self.list = []

        valid_chars = set("()|*") | self.alphabet
        if set(expression) - valid_chars != set():
            raise ValueError

    def diff_aut(self, automaton, suffix):
            aux_aut = Automaton({state + suffix for state in automaton.states},
                        automaton.alphabet, {}, automaton.init_state + suffix,
                        {frozenset([set(state).pop() + suffix])
                            for state in automaton.final_states})

            for state in automaton.transitions:
                key = frozenset([set(state).pop() + suffix])
                aux_aut.transitions[key] = {}
                for symbol in automaton.transitions[state]:
                    aux_aut.transitions[key][symbol] = set()
                    for element in automaton.transitions[state][symbol]:
                        aux_aut.transitions[key][symbol].add(
                            frozenset([set(element).pop() + suffix]))

            return aux_aut

    def add_transitions(self, automaton):
        for letter in automaton.alphabet:
            for state in automaton.transitions:
                try:
                    automaton.transitions[state][letter]
                except KeyError:
                    automaton.transitions[state][letter] = {}
                    automaton.transitions[state][letter] = set()

        return automaton

    def or_op(self, automatons):
        aut1 = self.diff_aut(automatons[0], "%")
        aut2 = self.diff_aut(automatons[1], "&")
        or_aut = Automaton({"initOr"}, set(),
                    {
                        frozenset(["initOr"]) : {
                            aut1.epsilon : set()
                        }
                    }, "initOr", set())

        for each in [aut1, aut2]:
            or_aut.states |= each.states
            or_aut.alphabet |= each.alphabet
            or_aut.transitions.update(each.transitions)
            or_aut.transitions[frozenset(["initOr"])][or_aut.epsilon].add(
                each.init_state)
            or_aut.final_states |= each.final_states

        return self.add_transitions(or_aut)

    def concat_op(self, automatons):
        aut1 = self.diff_aut(automatons[0], "#")
        aut2 = self.diff_aut(automatons[1], "$")
        concat_aut = Automaton(aut1.states | aut2.states,
                               aut1.alphabet | aut2.alphabet, {},
                               aut1.init_state, aut2.final_states)
        concat_aut.transitions.update(aut1.transitions)
        concat_aut.transitions.update(aut2.transitions)

        for state in aut1.final_states:
            try:
                concat_aut.transitions[state][concat_aut.epsilon].add(
                    frozenset([aut2.init_state]))
            except KeyError:
                concat_aut.transitions[state][concat_aut.epsilon] = set()
                concat_aut.transitions[state][concat_aut.epsilon].add(
                    frozenset([aut2.init_state]))

        return self.add_transitions(concat_aut)

    def closure_op(self, automatons):
        clsr_aut = Automaton(
                        {"initClsr"}, set(),
                        {
                            frozenset(["initClsr"]) : {
                                automatons[0].epsilon : set()
                            }
                        },
                        "initClsr", {frozenset(["initClsr"])})

        e = clsr_aut.epsilon
        for each in automatons:
            clsr_aut.states |= each.states
            clsr_aut.alphabet |= each.alphabet
            clsr_aut.transitions[frozenset(["initClsr"])][e].add(
                frozenset([each.init_state]))
            clsr_aut.transitions.update(each.transitions)
            clsr_aut.final_states |= each.final_states
            for state in each.final_states:
                try:
                    clsr_aut.transitions[state][e] = set()
                except KeyError:
                    clsr_aut.transitions[state] = {}
                    clsr_aut.transitions[state][e] = set()
                clsr_aut.transitions[state][e].add(frozenset(["initClsr"]))

        return self.add_transitions(clsr_aut)

    def single_state(self, transition):
        single_aut = Automaton(
                        {"q0" + transition, "q1" + transition}, {transition},
                        {
                            frozenset(["q0"+transition]) : {
                                transition : {frozenset(["q1"+transition])}
                            },
                            frozenset(["q1"+transition]) : {}
                        },
                        "q0" + transition, {frozenset(["q1"+transition])})
        return self.add_transitions(single_aut)

    def empty_word(self):
        return Automaton({"q0"}, set(), {}, "q0", {"q0"})

    def analyse_expression(self, expression):
        i = 0
        while len(expression) != 0:
            value = expression[i]
            if expression[i] in self.alphabet:
                self.list.append(expression[i])
                expression = expression[:i] + expression[i+1:]
            elif expression[i] == "|":
                _next = expression[i+1]
                if _next == "(":
                    aux = 2
                    while _next != ")":
                        _next = expression[i+aux]
                        if _next != ")":
                            self.list.append(_next)
                        aux += 1
                    expression = expression[:i] + expression[i+aux:]
                elif _next in self.alphabet:
                    after_next = expression[i+2]
                    if after_next == "*":
                        self.list.append(after_next)
                    self.list.append(_next)
                    expression = expression[:i] + expression[i+3:]
                self.list.append("|")
            elif expression[i] in ["(", ")", "*"]:
                if expression[i] == "*":
                    self.list.append("*")
                expression = expression[:i] + expression[i+1:]

    def execute_operations(self):
        partial_auts = []
        while len(self.list) != 0:
            char = self.list.pop(0)
            if char in self.alphabet:
                if len(partial_auts) == 2:
                    aux_list = [partial_auts.pop(0)]
                    aux_list.append(partial_auts.pop(0))
                    partial_auts.append(self.concat_op(aux_list))
                partial_auts.append(self.single_state(char))
            if char == "|":
                if len(partial_auts) == 3:
                    aux_list = [partial_auts.pop(1)]
                    aux_list.append(partial_auts.pop())
                    partial_auts.append(self.concat_op(aux_list))
                partial_auts = [self.or_op(partial_auts)]
            if char == "*":
                aut = [partial_auts.pop()]
                partial_auts.append(self.closure_op(aut))

        if len(partial_auts) == 2:
            return self.add_transitions(self.concat_op(partial_auts))
        return self.add_transitions(partial_auts.pop())

    def regular_to_automaton(self):
        self.analyse_expression(self.expression)
        return self.execute_operations()

def test():
    a = RegularExpression("(a|b)*")
    aux = a.regular_to_automaton()
    print("states:",aux.states)
    print("alphabet", aux.alphabet)
    pprint(aux.transitions)
    print("final:",aux.final_states)
    print("init:",aux.init_state)

test()