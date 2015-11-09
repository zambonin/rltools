#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""finite_automaton.py

Definition of a finite automaton and construction of deterministic finite
automata through the powerset construction method, also handling epsilon-moves.

Gustavo Zambonin & Matheus Ben-Hur de Melo Leite, UFSC, October 2015.
"""

from copy import deepcopy


class FiniteAutomaton(object):
    """A finite automaton is defined as a 5-tuple (Q, Σ, δ, q0, F) such that:
    Q is a finite set of states;
    Σ is a finite set of input symbols called the alphabet;
    δ : Q × Σ → Q (or, verbally, a transition function);
    q0 ∈ Q is a start state;
    F ⊆ Q is a set of accept states.
    """

    def __init__(self, states, alphabet, transitions, initstate, final_states):
        """Inits FiniteAutomaton with the attributes introduced above."""
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.init_state = initstate
        self.final_states = final_states
        self.epsilon = "ε"

    def __str__(self):
        """Pretty-prints the finite automaton object attributes."""
        states = "States: %s" % (', '.join(str(set([s])) for s in self.states))
        alphabet = "Alphabet: %s" % (', '.join(l for l in self.alphabet))
        transitions = "Transitions: "
        for t in self.transitions:
            transitions += '\n%s: %s' % (str(list(t)),
                                         str(self.transitions[t]))
        init_state = "Initial state: %s" % self.init_state
        final = "Final states: %s" % (', '.join(str(set(f))
                                                for f in self.final_states))
        return "%s\n%s\n%s\n%s\n%s" % (states, alphabet, transitions,
                                       init_state, final)

    def epsilon_closure(self):
        """Computes the epsilon-closure for each state of the input NFA.

        Returns:
            The set of every epsilon-closure of the NFA.
        """

        def single_closure(state):
            """Computes the epsilon-closure for a single state of a NFA.

            Arguments:
                state: the source state for the epsilon-closure computation.

            Returns:
                The epsilon-closure for said state.
            """
            closure, old_closure = {state, }, set()
            while old_closure != closure:
                old_closure = closure.copy()
                for state in old_closure:
                    try:
                        s = frozenset([state])
                        closure |= self.transitions[s][self.epsilon]
                    except KeyError:
                        pass
            return closure

        return {state: single_closure(state) for state in self.states}

    def determinize(self):
        """Modifies the input automaton in-place to be caracterized as a
        determinized finite automaton.
        """
        opened, closed, final_states = set(), set(), set()
        new_transitions = {}

        epsilon_closure = self.epsilon_closure()
        try:
            init_closure = epsilon_closure[frozenset([self.init_state])]
        except KeyError:
            init_closure = epsilon_closure[self.init_state]
        new_init_state = init_closure
        opened.add(frozenset(init_closure))

        while opened:
            state = opened.pop()
            closed.add(state)
            try:
                new_transition = {}
                for letter in self.transitions[state]:
                    new_transition[letter] = set()
                    for atom in self.transitions[state][letter]:
                        new_transition[letter] |= epsilon_closure[atom]
                new_transitions[state] = new_transition
            except KeyError:
                pass

            if state not in self.transitions.keys():
                aux_dict = {letter: set() for letter in self.alphabet}
                for atom in state:  # an atom is each part of a new state
                    for letter in self.alphabet:
                        aux = self.transitions[frozenset([atom])][letter]
                        for dest in aux:
                            aux_dict[letter] |= epsilon_closure[dest]
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
        """Modifies the input automaton in-place through an algorithm similar
        to Hopcroft's so the resulting DFA has the minimum number of states.
        """
        def belongs_to(self, state):
            """Auxiliar method for the partition refinement logic, also known
            as equivalence classes between states.

            Arguments:
                state: The state that may be placed in a new partition.

            Returns:
                A new partition with the respective states.
            """
            for lst in classes:
                if len(lst) > 1 or lst not in old_classes:
                    for letter in self.transitions[lst[0]]:
                        both = False
                        arrival_list = list()
                        arrival_list2 = list()
                        for old_list in old_classes:
                            head = lst.pop(0)
                            lst.insert(0, head)
                            if (frozenset(self.transitions[head][letter])
                               in old_list):
                                arrival_list = old_list
                            if (frozenset(self.transitions[state][letter])
                               in old_list):
                                arrival_list2 = old_list
                        if arrival_list == arrival_list2:
                            both = True
                        if not both:
                            break
                    if both:
                        return lst

            return [frozenset(state)]

        def assembler(self):
            """Constructs the minimal automaton from the equivalence classes
            computed previously.
            """
            i = 0
            new_states = set()
            mapping = {}
            new_init = ""
            new_transitions = {}
            new_finals = set()
            for classs in classes:
                i += 1
                new_states.add("q" + str(i))
                new_transitions[frozenset(["q" + str(i)])] = {}
                mapping[frozenset(classs)] = "q" + str(i)
            for classs in classes:
                for state in classs:
                    aux_class = ""
                    for classss in classes:
                        if state in classss:
                            aux_class = classss
                            break
                    if set(state).pop() in self.init_state:
                        new_init = str(mapping[frozenset(aux_class)])
                    if state in self.final_states:
                        new_finals.add(
                            frozenset([mapping[frozenset(aux_class)]]))
                    for letter in self.transitions[state]:
                        try:
                            new_transitions[frozenset([mapping[
                                frozenset(aux_class)]])][letter]
                            break
                        except KeyError:
                            new_transitions[frozenset([mapping[
                                frozenset(aux_class)]])][letter] = set()
                        piece = frozenset(self.transitions[state][letter])
                        another_aux_class = ""
                        for another_class in classes:
                            if piece in another_class:
                                another_aux_class = another_class
                                break
                        try:
                            new_transitions[frozenset([mapping[
                                frozenset(aux_class)]])][letter].add(
                                mapping[frozenset(another_aux_class)])
                        except KeyError:
                            pass

            self.transitions = new_transitions
            self.init_state = new_init
            self.final_states = new_finals
            self.states = new_states

        self.determinize()

        classes, old_classes = list(), list()
        classes.append(list(self.final_states))
        if len(list(self.states - self.final_states)) > 0:
            classes.append(list(self.states - self.final_states))

        while classes != old_classes:
            old_classes = deepcopy(classes)
            for classs in classes:
                if len(classs) > 1:
                    aux_c = classs[:]
                    head_state = aux_c.pop(0)
                    for state in aux_c:
                        index = classs.index(state)
                        classs.pop(index)
                        class_which_belongs = belongs_to(self, state)
                        if class_which_belongs in classes:
                            class_which_belongs.append(state)
                        else:
                            classes.append(class_which_belongs)

        assembler(self)
