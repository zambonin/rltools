#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Automaton:
    def __init__(self):
        self.states = set()
        self.transitions = {}
        self.alphabet = set()
        self.final_states = set()
        self.epsilon = "λ"
        self.new_states = set()
        self.new_transitions = {}

    def determinization(self):
        self.determinizer(self.epsilon_closure())
    
    def epsilon_closure(self):
        _epsilon_closure = {}
        for state in self.states:
            if self.epsilon in self.transitions[frozenset([state])]: 
                _epsilon_closure[state] = {state,} | self.transitions[frozenset([state])]["λ"]
            else:
                _epsilon_closure[state] = state
        return _epsilon_closure
   
    def determinizer(self, epsilon_closure):
        opened = set(frozenset([epsilon_closure[self.init_state]]))
        closed = set(frozenset())
        while opened:
            state = opened.pop()
            if type(state) is frozenset: #added to don't insert frozenset of frozenset
                closed.add(state)
            else:
                closed.add(frozenset([state]))
            if frozenset([state]) in self.transitions.keys():
                for key in self.transitions[frozenset([state])]:
                    aux_state = self.transitions[frozenset([state])][key]
                    new_state = set()
                    for atom in aux_state: #atom is each part of the aux state (if the state is an union of two or more states)
                        new_state.add(epsilon_closure[atom])
                    if new_state not in opened | closed:
                        opened.add(frozenset(new_state))
            else:
                self.create_transitions(state, epsilon_closure)
                

    def create_transitions(self, state, epsilon_closure):
        #TODO, create the transitions for the new state based on the union of the transitions from the states that
        #compose this one, remember to create a new dict of transitions to put this new ones and don't mix them with the 
        #transitions from the non-deterministic automaton
        self.transitions[state] = {}
        self.new_transitions[state] = {}
        aux_set = ()
        print("state : ", state)
        for atom in state: #atom is each part of the new state
            print("atom : ", atom)
            for letter in self.alphabet: #for each letter of the alphabet
                aux = self.transitions[frozenset([atom])][letter] #getting the transitions from atom by letter
                print("auxiliar : ", aux, "by letter : ", letter)
                if len(aux) > 1: #if the atom by the letter transits to more than one state
                    print("len is greater : ", len(aux))
                    for atom in aux: #getting the states that the atom transits by the letter to
                        aux_set.add(epsilon_closure[atom]) #adding the epsilon closure from that arrival state to the aux_set
                        print("aux set after addinf atom of atom : ", aux_set)
                else:
                    if aux: #if the atom by the letter transits to just one state
                        aux_set.add(epsilon_closure[aux.pop()]) #popping that state from the set aux and adding their epsilon-closure to the aux_set
                self.transitions[state][letter] = aux_set
                print("trazii : ", self.transitions[state])
                self.new_transitions[state][letter] = aux_set
                print("aux set : ", aux_set)
            aux_set.clear() #cleaning the set for the next iteration with another letter
        print("transitions : ", self.transitions[state])






def test():
    a = Automaton()
    a.states.add("q0")
    a.states.add("q1")
    a.states.add("q2")
    a.states.add("q3")

    a.init_state = "q0"
    a.final_states.add("q3")
    
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
test()
