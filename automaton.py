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
                    final_states.add(new_state)
        self.final_states = final_states
        self.init_state = new_init_state
        self.states.clear()
        for state in new_transitions:
            self.states.add(state)
        self.transitions = new_transitions

    def minimize(self):
        self.determinize()
        """for state in self.transitions:
            for letter in self.transitions[state]:
                if len(self.transitions[state][letter]) > 1 or letter == self.epsilon:
                    self.determinize()
                    break
                else:
                    continue
                break"""

        def belongs_to(self, state, number_list):
            for lst in classes:
                if classes.index(lst) != number_list and len(lst) > 1:
                    for letter in self.transitions[lst[0]]:
                        both = False
                        arrival_list = list()
                        arrival_list2 = list()
                        for old_list in old_classes:
                            head = lst.pop(0)
                            lst.insert(0, head)
                            if frozenset(self.transitions[head][letter]) in old_list:
                                arrival_list = old_list
                            if frozenset(self.transitions[state][letter]) in old_list:
                                arrival_list2 = old_list

                        if arrival_list == arrival_list2:
                            both = True
                        if not both:
                            break
                    if both:
                        return lst
            return [frozenset(state)]

        classes = list()
        classes.append(list(self.final_states))
        classes.append(list(self.states - self.final_states))

        old_classes = list()


        while classes != old_classes:
            old_classes = classes
            for classs in classes:
                if len(classs) > 1:
                    for i in range(1,len(classs)-1):
                        state = classs.pop(i)
                        class_which_belongs = belongs_to(self, state, i)
                        if class_which_belongs in classes:
                            class_which_belongs.append(state)
                        else:
                            classes.append(class_which_belongs)

        print (classes)





def test():
     b = Automaton(set(), set(), {}, "0", set())
     b.states.add("S")
     b.states.add("A")
     b.states.add("B")
     b.states.add("C")
     b.states.add("D")

     b.init_state = "S"
     b.final_states.add(frozenset(["A"]))
     b.final_states.add(frozenset(["B"]))
     b.final_states.add(frozenset(["C"]))
     b.final_states.add(frozenset(["D"]))

     b.transitions[frozenset(["S"])] = {}
     b.transitions[frozenset(["S"])]["a"] = {"A", "C", "D"}
     b.transitions[frozenset(["S"])]["b"] = {"A", "B", "C"}

     b.transitions[frozenset(["A"])] = {}
     b.transitions[frozenset(["A"])]["a"] = set()
     b.transitions[frozenset(["A"])]["b"] = {"A", "B"}

     b.transitions[frozenset(["B"])] = {}
     b.transitions[frozenset(["B"])]["a"] = {"A"}
     b.transitions[frozenset(["B"])]["b"] = {"B"}

     b.transitions[frozenset(["C"])] = {}
     b.transitions[frozenset(["C"])]["a"] = {"C","D"}
     b.transitions[frozenset(["C"])]["b"] = set()

     b.transitions[frozenset(["D"])] = {}
     b.transitions[frozenset(["D"])]["a"] = {"D"}
     b.transitions[frozenset(["D"])]["b"] = {"C"}

     b.alphabet.add("a")
     b.alphabet.add("b")

     b.minimize()
test()