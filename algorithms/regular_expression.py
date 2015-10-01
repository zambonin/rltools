#!/usr/bin/env python
#-*- coding: utf-8 -*-

from algorithms.finite_automaton import FiniteAutomaton

from pprint import pprint

class RegularExpression:
    def automaton_to_regexp(automaton):
        states = automaton.states
        transitions = automaton.transitions

        initial, final = 'i', 'f'
        states = {initial,final, frozenset()} | states

        init_state = automaton.init_state
        final_states = [set(x) for x in automaton.final_states]

        expr = {}
        for x in states:
            for y in states:
                expr[x,y] = None

        expr['i', frozenset(init_state)] = automaton.epsilon

        for x in final_states:
            expr[frozenset(x), 'f'] = automaton.epsilon

        old_transitions = transitions.copy()
        transitions.clear()

        for i in old_transitions:
            transitions[frozenset(list(i)[0].split(','))] = old_transitions[i]
            # del transitions[i]

        pprint(expr)

        for x in transitions:
            for t in transitions[x]:
                # print(transitions[x][t])
                print(x, transitions[x][t], frozenset(transitions[x][t]))
                expr[x, frozenset(transitions[x][t])] = t

        # pprint(expr)

        # states_copy = states.copy()

        # print(states)

        while len(states) > 2:
            s = next(x for x in states if isinstance(x, frozenset))
            # print(states)
            # print(s)
            for x in states:
                for y in states:
                    print(x, s, expr[x, s])
                    if expr[x, s] and expr[s, y] and x != s and y != s:
                        l1 = expr[x, s]
                        l2 = expr[s, s]
                        l3 = expr[s, y]
                        l4 = expr[x, y]

                        if not l2 and not l4:
                            part_re = "(%s)(%s)" % (l1, l3)
                        elif l2 and l4:
                            part_re = "((%s)(%s)*(%s))|%s" % (l1, l2, l3, l4)
                        elif not l2 and l4:
                            part_re = "(%s)(%s)|%s" % (l1, l3, l4)
                        elif not l4 and l2:
                            part_re = "(%s)(%s)*(%s)" % (l1, l2, l3)

                        expr[x, y] = part_re
                        # print(part_re)
            states.remove(s)

        print(expr['i', 'f'])
                            


        # pprint(expr)
        # for x in states:
        #     for t in transitions:

