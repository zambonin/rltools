#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from copy import deepcopy
from finite_automaton import FiniteAutomaton
from regular_grammar import RegularGrammar

def load(path):
    def handle_transitions(old_dict):
        new = {frozenset([i]) : old_dict[i] for i in old_dict}
        for i in new:
            for j in new[i]:
                new[i][j] = set(new[i][j])
        return new

    with open(path) as file_in:
        data = json.load(file_in)
        header = data['type']

        if header == 'automaton':
            return FiniteAutomaton(set(data['states']), set(data['alphabet']),
                                   handle_transitions(data['transitions']),
                                   data['init_state'],
                                   {frozenset(data['final_states'])})

        if header == 'grammar':
            return RegularGrammar(set(data['non_terminals']),
                                  set(data['terminals']),
                                  {i : set(data['productions'][i])
                                            for i in data['productions']},
                                  data['init_production'])

def save(path, header, obj):
    obj = deepcopy(obj)
    with open(path, 'w', encoding='utf8') as file_out:
        if header == 'automaton':
            json.dump({
                        'type' : 'automaton',
                        'states' : [list(i) for i in obj.states],
                        'alphabet' : list(obj.alphabet),
                        'transitions' : {str(list(i)) : list(i)
                                            for i in obj.transitions},
                        'init_state' : tuple(obj.init_state),
                        'final_states' : [list(i) for i in obj.final_states]
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

