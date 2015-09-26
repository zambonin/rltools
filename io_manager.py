#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from automaton import Automaton

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
            return Automaton(set(data['states']),
                             set(data['alphabet']),
                             handle_transitions(data['transitions']),
                             data['init_state'],
                             {frozenset(data['final_states'])})

def save(path, header, obj):
    def handle_transitions(old_dict):
        new = {str(list(i)) : old_dict[i] for i in old_dict}
        for i in new:
            for j in new[i]:
                new[i][j] = list(new[i][j])
        return new

    with open(path, 'w', encoding='utf8') as file_out:
        if header == 'automaton':
            json.dump({
                    'type' : 'automaton',
                    'states' : [list(i) for i in obj.states],
                    'alphabet' : list(obj.alphabet),
                    'transitions' : handle_transitions(obj.transitions),
                    # 'init_state' : [obj.init_state],
                    # 'final_states' : obj.final_states
                    }, file_out, indent=4, ensure_ascii=False)
