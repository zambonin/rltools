#!/usr/bin/env python
# -*- coding: utf-8 -*-

from finite_automaton import FiniteAutomaton

class RegularGrammar:
    def __init__(self, non_terminals, terminals, productions, init_production):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.init_production = init_production

    def __str__(self):
        non_term = "Non-terminals: %s" % (', '.join(
                                          nt for nt in self.non_terminals))
        terminals = "Terminals: %s" % (', '.join(
                                       t for t in self.terminals))

        grammar = "Grammar: "
        for prod in self.productions:
            grammar += "\n[" + prod + "]" + " -> "
            grammar += " | ".join([p for p in self.productions[prod]])

        init_prod = "Initial production: " + self.init_production

        return "%s\n%s\n%s\n%s" % (terminals, non_term, init_prod, grammar)

    def automaton_to_grammar(aut):
        non_terminals = aut.alphabet
        terminals = set()
        productions = {}
        init_production = "".join(part.upper() for part in aut.init_state)

        for state in aut.transitions:
            terminal = "".join(part.upper() for part in state)
            productions[terminal] = set()
            terminals.add(terminal)
            for letter in aut.transitions[state]:
                aux = "".join(i.upper() for i in aut.transitions[state][letter])
                if aux != "":
                    productions[terminal].add(letter + aux)
                if aut.transitions[state][letter] in aut.final_states:
                    productions[terminal].add(letter)

        return RegularGrammar(non_terminals, terminals,
                              productions, init_production)

    def grammar_to_automaton(gram):
        states, final_states = set(), set()
        alphabet = gram.non_terminals
        transitions = {}
        initial_state = gram.init_production.lower()

        for production in gram.productions:
            states.add(production.lower())
            transitions[frozenset([production.lower()])] = {}

            for part in gram.productions[production]:
                if len(part) > 1:
                    transitions[frozenset([production.lower()])][part[0]] = part[1:].lower()

            for part in gram.productions[production]:
                if len(part) == 1:
                    final_states.add(transitions[frozenset([production.lower()])][part])

            if len(gram.productions[production]) == 0:
                for symbol in alphabet:
                    transitions[frozenset([production.lower()])][symbol] = set()

        return FiniteAutomaton(states, alphabet, transitions,
                               initial_state, final_states)
