#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint

class Automaton:
    def __init__(self, states, alphabet, transitions,
                 init_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.init_state = init_state
        self.final_states = final_states
        self.epsilon = "ε"

    def determinize(self):
        self.NFAtoDFA(self.epsilon_closure())

    def epsilon_closure(self):
        def single_closure(state):
            closure, old_closure = {state,}, set()
            while old_closure != closure:
                old_closure = closure.copy()
                for state in old_closure:
                    try:
                        s = frozenset([state])
                        closure |= self.transitions[s][self.epsilon]
                    except KeyError:
                        pass
            return closure

        return {state : single_closure(state) for state in self.states}

    def NFAtoDFA(self, epsilon_closure):
        init_closure = epsilon_closure[self.init_state]
        new_init_state = init_closure

        opened, closed, final_states = set(), set(), set()
        opened.add(frozenset(init_closure))

        new_transitions = {}

        while opened:
            state = opened.pop()
            closed.add(state)
            try:
                new_transitions[state] = self.transitions[state]
            except KeyError:
                pass

            if state not in self.transitions.keys():
                aux_dict = {letter: set() for letter in self.alphabet}
                for atom in state: # an atom is each part of a new state
                    for letter in self.alphabet:
                        aux = self.transitions[frozenset([atom])][letter] # getting the transitions from atom by letter
                        for dest in aux: # getting the states that the atom transits to, by said letter
                            aux_dict[letter] |= epsilon_closure[dest] # adding the epsilon closure from that arrival state to the aux_set
                self.transitions[state] = aux_dict
                new_transitions[state] = aux_dict

            for key in self.transitions[state]:
                aux_state, new_state = self.transitions[state][key], set()
                for atom in aux_state:
                    new_state |= epsilon_closure[atom]
                if new_state not in opened | closed and new_state:
                    opened.add(frozenset(new_state))
                    try:
                        ns = frozenset(new_state)
                        new_transitions[ns] = self.transitions[ns]
                    except KeyError:
                        pass

        for state in self.final_states:
            for new_state in new_transitions:
                if state & new_state:
                    final_states |= new_state
        # multiple final states problem (?)
        self.final_states = final_states
        self.init_state = new_init_state
        self.states.clear()
        for state in new_transitions:
            self.states.add(state)
        self.transitions = new_transitions

# def test(flag=False):
#     states = set(['q0', 'q1', 'q2', 'q3'])
#     alphabet = set(['a', 'b'])
#     transitions = {
#         frozenset(['q0']) : {
#             'a' : {'q0', 'q1'},
#             'b' : {'q0'},
#         },
#         frozenset(['q1']) : {
#             'a' : {'q2'},
#             'b' : set(),
#         },
#         frozenset(['q2']) : {
#             'a' : set(),
#             'b' : {'q3'},
#         },
#         frozenset(['q3']) : {
#             'a' : {'q3'},
#             'b' : {'q3'},
#         }
#     }
#     init_state = "q0"
#     final_states = {frozenset(['q3'])}

#     a = Automaton(states, alphabet, transitions, init_state, final_states)
#     a.determinize()

#     if flag:
#         print("Transitions")
#         pprint(a.transitions)
#         print("Initial :",a.init_state)
#         print("States")
#         pprint(a.states)
#         print("Finals")
#         pprint(a.final_states)

# def test2(flag=False):
#     states = set(['p', 'q', 'r', 's'])
#     alphabet = set(['a', 'b', 'c'])
#     transitions = {
#         frozenset(['p']) : {
#             'ε' : {'p', 'q'},
#             'a' : set(),
#             'b' : {'q'},
#             'c' : {'r'},
#         },
#         frozenset(['q']) : {
#             'a' : {'p'},
#             'b' : {'r'},
#             'c' : {'p', 'q'},
#         },
#         frozenset(['r']) : {
#             'a' : set(),
#             'b' : set(),
#             'c' : set(),
#         }
#     }
#     init_state = 'p'
#     final_states = {frozenset(['r'])}

#     b = Automaton(states, alphabet, transitions, init_state, final_states)
#     b.determinize()

#     if flag:
#         print("Transitions")
#         pprint(b.transitions)
#         print("Initial :",b.init_state)
#         print("States")
#         pprint(b.states)
#         print("Finals")
#         pprint(b.final_states)

# def test3(flag=False):
#     states = set(['x', 'y', 'z'])
#     alphabet = set(['0', '1'])
#     transitions = {
#         'x' : {
#             '0' : {'x', 'y'},
#             '1' : {'x'},
#         },
#         'y' : {
#             '0' : set(),
#             '1' : {'z'},
#         },
#         'z' : {
#             '0' : set(),
#             '1' : set(),
#         }
#     }
#     init_state = 'x'
#     final_states = {frozenset(['z'])}

#     c = Automaton(states, alphabet, transitions, init_state, final_states)
#     c.determinize()

#     if flag:
#         print("Transitions")
#         pprint(c.transitions)

#         print("Initial:", c.init_state)

#         print("States")
#         pprint(c.states)

#         print("Finals:", c.final_states)

# test(True); print()
# test2(True); print()
# test3(True)
