#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint
class Automaton:
    def __init__(self):
        self.states = set()
        self.transitions = {}
        self.alphabet = set()
        self.final_states = set()
        self.epsilon = "λ"
        self.new_transitions = {}

    def determinization(self):
        self.determinized(self.epsilon_closure())
    
    def epsilon_closure(self):
        def single_epsilon_closure(state):
            epsilon_c = {state,}
            old_epsilon_c = set()
            while old_epsilon_c != epsilon_c:
                old_epsilon_c = epsilon_c.copy()
                for state in old_epsilon_c:
                    try:
                        epsilon_c.update(self.transitions[frozenset([state])][self.epsilon])
                    except KeyError:
                        pass
            return epsilon_c

        _epsilon_closure = {}
        for state in self.states:
            _epsilon_closure[state] = single_epsilon_closure(state)
        return _epsilon_closure

   
    def determinized(self, epsilon_closure):
        closure_initial, opened = epsilon_closure[self.init_state], set()
        if isinstance(closure_initial, str):
            opened.add(frozenset([closure_initial]))
            self.new_init_state = closure_initial
        else:
            opened.add(frozenset(closure_initial))
            self.new_init_state = closure_initial
        closed = set(frozenset())
        while opened:
            state = opened.pop()
            if type(state) is not frozenset: #added to don't insert frozenset of frozenset
                state = frozenset([state])
                closed.add(state)
                try:
                    self.new_transitions[state] = self.transitions[state]
                except KeyError:
                    pass
            else:
                closed.add(state)
                try:
                    self.new_transitions[state] = self.transitions[state]
                except KeyError:
                    pass
            if state in self.transitions.keys():
                for key in self.transitions[state]:
                    aux_state = self.transitions[state][key]
                    new_state = set()
                    for atom in aux_state: #atom is each part of the aux state (if the state is an union of two or more states)
                        try:
                            new_state.add(epsilon_closure[atom])
                        except TypeError:
                            new_state.update(epsilon_closure[atom])
                    if new_state not in opened | closed and new_state:
                        opened.add(frozenset(new_state))
                        try:
                            self.new_transitions[frozenset(new_state)] = self.transitions[frozenset(new_state)]
                        except KeyError:
                            pass
            else:
                self.create_transitions(state, epsilon_closure)
                for key in self.transitions[state]:
                    aux_state = self.transitions[state][key]
                    new_state = set()
                    for atom in aux_state: #atom is each part of the aux state (if the state is an union of two or more states)
                        try:
                            new_state.add(epsilon_closure[atom])
                        except TypeError:
                            new_state.update(epsilon_closure[atom])
                    if new_state not in opened | closed and new_state:
                        opened.add(frozenset(new_state))
                        try:
                            self.new_transitions[frozenset(new_state)] = self.transitions[frozenset(new_state)]
                        except KeyError:
                            pass
        self.create_dfa()

    def create_dfa(self):
        final_states = set()
        for state in self.final_states:
            for new_state in self.new_transitions:
                if state & new_state:
                    final_states.add(new_state)
        self.final_states = final_states
        self.init_state = self.new_init_state
        self.states.clear()
        for state in self.new_transitions:
            self.states.add(state)

        self.transitions = self.new_transitions




    def create_transitions(self, state, epsilon_closure):
        aux_dict = {letter: set() for letter in self.alphabet} #creating an empty dict with the alphabet letter keys
        for single in state: #atom is each part of the new state
            for letter in self.alphabet: #for each letter of the alphabet                
                aux = self.transitions[frozenset([single])][letter] #getting the transitions from atom by letter
                for atom2 in aux: #getting the states that the atom transits by the letter to
                    try:
                        aux_dict[letter].add(epsilon_closure[atom2]) #adding the epsilon closure from that arrival state to the aux_set
                    except TypeError:
                        aux_dict[letter].update(epsilon_closure[atom2])
                        
        self.transitions[state] = aux_dict
        self.new_transitions[state] = aux_dict



def test():
    a = Automaton()
    a.states.add("q0")
    a.states.add("q1")
    a.states.add("q2")
    a.states.add("q3")

    a.init_state = "q0"
    a.final_states.add(frozenset(["q3"]))
    
    q0 = frozenset(["q0"])
    a.transitions[q0] = {}
    a.transitions[q0]["a"] = {"q0", "q1"} 
    a.transitions[q0]["b"] = {"q0"}
    
    a.transitions[frozenset(["q1"])] = {}
    a.transitions[frozenset(["q1"])]["a"] = {"q2"}
    a.transitions[frozenset(["q1"])]["b"] = set()

    a.transitions[frozenset(["q2"])] = {}
    a.transitions[frozenset(["q2"])]["a"] = set()
    a.transitions[frozenset(["q2"])]["b"] = {"q3"}
    
    a.transitions[frozenset(["q3"])] = {}
    a.transitions[frozenset(["q3"])]["a"] = {"q3"}
    a.transitions[frozenset(["q3"])]["b"] = {"q3"}
    

    a.alphabet.add("a")
    a.alphabet.add("b")
    a.determinization()

    print("Transitions")
    pprint(a.transitions)
    print("Initial :",a.init_state)
    print("States")
    pprint(a.states)
    print("Finals")
    pprint(a.final_states)

    b = Automaton()
    b.states.add("p")
    b.states.add("q")
    b.states.add("r")
    b.states.add("s")

    b.init_state = "p"
    b.final_states.add(frozenset("r"))
    
    b.transitions[frozenset(["p"])] = {}
    b.transitions[frozenset(["p"])]["λ"] = {"p","q"}
    b.transitions[frozenset(["p"])]["a"] = set()
    b.transitions[frozenset(["p"])]["b"] = {"q"}
    b.transitions[frozenset(["p"])]["c"] = {"r"}

    b.transitions[frozenset(["q"])] = {}
    b.transitions[frozenset(["q"])]["λ"] = {"r"}
    b.transitions[frozenset(["q"])]["a"] = {"p"}
    b.transitions[frozenset(["q"])]["b"] = {"r"}
    b.transitions[frozenset(["q"])]["c"] = {"p","q"}

    b.transitions[frozenset(["r"])] = {}
    b.transitions[frozenset(["r"])]["a"] = set()
    b.transitions[frozenset(["r"])]["b"] = set()
    b.transitions[frozenset(["r"])]["c"] = set()


    b.transitions[frozenset(["s"])] = {}
    b.transitions[frozenset(["r"])]["λ"] = {"s"}
    b.transitions[frozenset(["s"])]["a"] = set()
    b.transitions[frozenset(["s"])]["b"] = set()
    b.transitions[frozenset(["s"])]["c"] = set()

    b.alphabet.add("a")
    b.alphabet.add("b")
    b.alphabet.add("c")
    b.determinization()
    print("Transitions")
    pprint(b.transitions)
    print("Initial :",b.init_state)
    print("States")
    pprint(b.states)
    print("Finals")
    pprint(b.final_states)

test()
