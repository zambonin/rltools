#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict

class Determinizer:
    def __init__(self):
        self.automata = {}
        self.epsilon = 'λ'
        self.init_marker = 'α'
        self.final_marker = 'ω'
    
    def determinization(self, automata):
        def epsilon_determinizer(automata):
            print('banana2')

        def simple_determinizer(automata):            
            opened, closed, new_states = [], [], []

            for key in automata.keys():
                if self.init_marker in automata[key]:
                    opened.append({key: automata[key]})

            for state in opened:
                for transition in state:
                    print(transition)
                    for j in state[transition]:
                        if len(j) > 1 and j[1] not in opened + closed:
                                opened.append({j : []})
                closed.append(opened.pop(0))
            print(opened)
            print(closed)       
 
            # for state in opened:
                # grp_transit = find_equal_transitions(state)
                # if grp_transit:
                    # new_state = list(set([grp_transit[i] for i
                    #                  in grp_transit.keys()]))[0]
                    # new_states.append(new_state)
                    # closed.append(opened.pop(0))
                # for i in state:

            #     for i in a.keys():
            #         opened.append({a[i]:'a'})
            # poss_letters = []
            # for i in opened:
            #     for transition in i:
            #         if len(transition) > 1:
            #             poss_letters += transition[0]
            # unique_transitions = list(set(poss_letters))
            # if poss_letters != unique_transitions:
            #     for i in unique_transitions:
                    

                    
            # while opened:
            #     actual_state = opened.pop(0)
            #     print(actual_state)
            #     for transition in actual_state:
            #         if len(transition) > 1 and \
            #             transition[1] not in opened + closed:
            #             opened.append(automata[transition[1]])
            #     closed.append(actual_state)

            # return closed

        # def find_equal_transitions(state):
        #     d = defaultdict(tuple)
        #     for transition, destination in state[1:]:
        #         if state[0] == self.final_marker:
        #             d += state[0]
        #         d[transition] += (destination,)
        #     # print(list(d.items()))
        #     return dict((k,v) for (k,v) in d.items() if len(v) > 1)

        # for state in automata.keys():
            # print(find_equal_transitions(automata[state]))
            
            # print(automata[state])

        epsilon_test = []
        for key in automata.keys():
            epsilon_test += [i for i in automata[key] if self.epsilon in i]
        
        if epsilon_test:
            return epsilon_determinizer(automata)
        return simple_determinizer(automata)
    

    def test(self):
        # test_automata = {
        #    'q0' : [self.init_marker, ('0', 'q0'), ('0', 'q1'), ('1', 'q0')], 
        #    'q1' : [('0', 'q2')],
        #    'q2' : [('1', 'q3')],
        #    'q3' : [self.final_marker],
        # }
        # maybe TODO method test1 -> test2
        test2 = {
           'q0' : [self.init_marker, ('0', ('q0', 'q1')), ('1', ('q0'))],
           'q1' : [('0', 'q2')],
           'q2' : [('1', 'q3')],
           'q3' : [self.final_marker],
        }
        return test2

p = Determinizer()
a = p.test()

p.determinization(a)
