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
                    'init_state' : tuple(obj.init_state),
                    'final_states' : [list(i) for i in obj.final_states]
                    }, file_out, indent=4, ensure_ascii=False)

aut = load('test.in')
aut.determinize()
save('output.out', 'automaton', aut)

aut = load('test2.in')
aut.determinize()
save('output2.out', 'automaton', aut)

aut = load('test3.in')
aut.determinize()
save('output3.out', 'automaton', aut)
