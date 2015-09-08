#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Automaton:
    def __init__(self):
        self.states = set()
        self.transitions = {}
        self.alphabet = set()
        self.final_states = set()
        self.epsilon = 'λ'
        #self.init_marker = 'α'
        #self.final_marker = 'ω'
    
    def determinization(self):
        for word in self.transitions:
            if word[1] == self.epsilon:
                return self.epsilon_determinizer()
        return self.simple_determinizer()

    def simple_determinizer(self):
        opened = {(self.init_state,)} #I'm creating a state and forcing a tuple into it
        closed = set()
        while opened:
            state = opened.pop()
            closed.add(tuple(state))
            for transition in self.transitions:
                if transition[0] == state[0]:   #If this statement is true, the loop breaks
                    break
            else:                       
                create_transitions(state)    
            for transition in self.transitions:
                if transition[0] == state[0]:
                    if tuple(self.transitions[transition]) not in opened | closed:
                       opened.add(tuple(self.transitions[transition]))
            print(closed)
    
    def epsilon_determinizer(self):
        pass
    def create_transitions(self, state)
        #TODO, create the transitions for the new state based on the union of the transitions from the states that
        #compose this one, remember to create a new dict of transitions to put this new ones and don't mix them with the 
        #transitions from the non-deterministic automaton
        pass
def test():
    a = Automaton()
    a.states.add("q0")
    a.states.add("q1")
    a.states.add("q2")
    a.states.add("q3")

    a.init_state = "q0"
    a.final_states.add("q3")

    a.transitions[("q0", "a")] = {"q0", "q1"}
    a.transitions[("q0","b")] = {"q0",}
    a.transitions[("q1", "a")] = {"q2"}
    a.transitions[("q2","b")] = {"q3",}
    a.transitions[("q3", "a")] = {"q3",}
    a.transitions[("q3","b")] = {"q3",}


    a.alphabet.add("a")
    a.alphabet.add("b")
    a.determinization()

test()