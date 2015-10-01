#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""io_manager.py

Tool for loading and saving objects as JSON files.

Gustavo Zambonin & Matheus Ben-Hur de Melo Leite, UFSC, October 2015.
"""

import json
from copy import deepcopy
from algorithms.finite_automaton import FiniteAutomaton
from algorithms.regular_grammar import RegularGrammar

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

    def handle_states(old_list, old_init, old_final):
        def handle_list(old):
            new = []
            for i in old:
                if len(i) > 1 and not isinstance(i, frozenset):
                    new.append(i.split(','))
                else:
                    new.append(list(i))
            return new

        def handle_init(oldl, oldi):
            if oldi in list(oldl):
                if isinstance(oldi, set):
                    return list(oldi)
                elif isinstance(oldi, str):
                    return [oldi]
            elif ",".join(oldi) in oldl:
                return list(set(oldi))

        return handle_list(old_list), handle_init(old_list, old_init), handle_list(old_final)

    obj = deepcopy(obj)
    with open(path, 'w', encoding='utf8') as file_out:
        if header == 'automaton':
            t = handle_states(obj.states, obj.init_state, obj.final_states)
            json.dump({
                        'type' : 'automaton',
                        'states' : t[0],
                        'alphabet' : list(obj.alphabet),
                        'transitions' : handle_transitions(obj.transitions),
                        'init_state' : t[1],
                        'final_states' : t[2],
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

        if header == 'regexp':
            json.dump({
                      'type' : 'regexp',
                      'expression' : obj,
                      }, file_out, indent=4, ensure_ascii=False)