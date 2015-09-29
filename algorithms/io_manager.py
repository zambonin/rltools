#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from copy import deepcopy
from algorithms.finite_automaton import FiniteAutomaton
from algorithms.regular_grammar import RegularGrammar

"""io_manager.py

Tool for loading and saving objects as JSON files.

Gustavo Zambonin & Matheus Ben-Hur de Melo Leite, UFSC, October 2015.
"""

def load(path):
    def handle_states(states):
        if isinstance(states[0], list):
            return {frozenset(i) for i in states}
        return set(states)

    def handle_transitions(old_dict):
        new = {frozenset([i]) : old_dict[i] for i in old_dict}
        for i in new:
            for j in new[i]:
                new[i][j] = set(new[i][j])
        return new

    def handle_final(final_s):
        new = set()
        for i in final_s:
            if isinstance(i, list):
                new.add(frozenset(i))
            else:
                new.add(frozenset([i]))
        return new

    with open(path) as file_in:
        data = json.load(file_in)
        header = data['type']

        if header == 'automaton':
            return FiniteAutomaton(handle_states(data['states']),
                                   data['alphabet'],
                                   handle_transitions(data['transitions']),
                                   data['init_state'],
                                   handle_final(data['final_states']))

        if header == 'grammar':
            return RegularGrammar(set(data['non_terminals']),
                                  set(data['terminals']),
                                  {i : set(data['productions'][i])
                                            for i in data['productions']},
                                  data['init_production'])

def save(path, header, obj):
    def handle_transitions(old_dict):
        new = {",".join(l for l in list(i)) : old_dict[i] for i in old_dict}
        for i in new:
            for j in new[i]:
                if isinstance(new[i][j], set):
                    new[i][j] = list(new[i][j])
                else:
                    new[i][j] = new[i][j].split(',')
        return new

    def handle_states(old_list):
        new = []
        for i in old_list:
            if len(i) > 1 and not isinstance(i, frozenset):
                new.append(i.split(','))
            else:
                new.append(list(i))
        return new

    def handle_init(state):
        if isinstance(state, set):
            return list(state)[0]
        return state

    obj = deepcopy(obj)
    with open(path, 'w', encoding='utf8') as file_out:
        if header == 'automaton':
            json.dump({
                        'type' : 'automaton',
                        'states' : handle_states(obj.states),
                        'alphabet' : list(obj.alphabet),
                        'transitions' : handle_transitions(obj.transitions),
                        'init_state' : handle_init(obj.init_state),
                        'final_states' : handle_states(obj.final_states)
                    }, file_out, indent=4, ensure_ascii=False)

        if header == 'grammar':
            json.dump({
                        'type' : 'grammar',
                        'non_terminals' : list(obj.non_terminals),
                        'terminals' : list(obj.terminals),
                        'productions' : {i : list(obj.productions[i])
                                            for i in obj.productions},
                        'init_production' : obj.init_production,
                      }, file_out, indent=4, ensure_ascii=False)
