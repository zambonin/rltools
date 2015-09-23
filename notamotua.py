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
        determinizer(self.epsilon_closure())
    
    def epsilon_closure(self):
        _epsilon_closure = {}
        for state in self.states:
            if self.epsilon in self.transitions[frozenset([state])]: 
                _epsilon_closure[state] = state | self.transitions[frozenset([state])]["λ"]
            else:
                _epsilon_closure[state] = state
        return _epsilon_closure
    
    #The code below is wrong!!!
    def simple_determinizer(self):
        opened = {(self.init_state,)} #I'm creating a state and forcing a tuple into it
        closed = set()
        while opened:
            state = opened.pop()
            closed.add(tuple(state))
            for transition in self.transitions:
                print("transition : ", transition)
                if transition[0] == state[0]:   #If this statement is true, the loop breaks
                    break
                else:                       
                    print("Creating transitions", state)
                    self.create_transitions(state)
                    #self.transitions = self.transitions and self.new_transitions
                for transition in self.transitions:
                    if transition[0] == state[0]:
                        if tuple(self.transitions[transition]) not in opened | closed:
                            opened.add(tuple(self.transitions[transition]))
            print("Closed : ", closed)
            print("Opened : ", opened)
    
    def epsilon_determinizer(self):
        pass

    def create_transitions(self, state):
        #TODO, create the transitions for the new state based on the union of the transitions from the states that
        #compose this one, remember to create a new dict of transitions to put this new ones and don't mix them with the 
        #transitions from the non-deterministic automaton
        self.new_states.add(state)
        for letter in self.alphabet:
            auxiliar_set = set()
            for element in state:
                auxiliar_set = auxiliar_set | self.transitions[(element, letter)] 
            self.new_transitions[(state,letter)] = auxiliar_set
        print("New transitions : ", self.new_transitions) 
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
    a.transitions[frozenset(["q1"])]["b"] = {"q3"}
    

    a.alphabet.add("a")
    a.alphabet.add("b")
    print(a.epsilon_closure())
    #a.determinization()
test()
