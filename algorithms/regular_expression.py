#!/usr/bin/env python
#-*- coding: utf-8 -*-

from algorithms.finite_automaton import FiniteAutomaton

class RegularExpression:
    def automaton_to_regexp(automaton):
        transitions = automaton.transitions
        states = {'i', 'f', frozenset()} | automaton.states
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

        for x in transitions:
            for t in transitions[x]:
                expr[x, frozenset(transitions[x][t])] = t

        while len(states) > 2:
            s = next(x for x in states if isinstance(x, frozenset))
            for x in states:
                for y in states:
                    if expr[x, s] is not None and expr[s, y] is not None and x != s and y != s:
                        l1 = expr[x, s]
                        l2 = expr[s, s]
                        l3 = expr[s, y]
                        l4 = expr[x, y]

                        print(l1, l2, l3, l4)

                        if l2 == None and l4 == None:
                            part_re = "(%s)(%s)" % (l1, l3)
                        elif l2 is not None and l4 is not None:
                            part_re = "((%s)(%s)*(%s))|%s" % (l1, l2, l3, l4)
                        elif l2 == None and l4 is not None:
                            part_re = "(%s)(%s)|%s" % (l1, l3, l4)
                        elif l4 == None and l2 is not None:
                            part_re = "(%s)(%s)*(%s)" % (l1, l2, l3)

                        expr[x, y] = part_re
            states.remove(s)

        return expr['i', 'f']
