#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ll_parser.py

Simple implementation of a LL(1) parser, with the grammar produced by hand.

Gustavo Zambonin & Matheus Ben-Hur de Melo Leite, UFSC, November 2015.
"""


class Parser(object):
    def __init__(self):
        master = {
            "<S>": {
                'program':    'program ; <INST> begin <PROGRAM> ;'
            },
            "<INST>": {
                'type':       'type identifier = <CONTENT> ; <INST>',
                'begin':      'ε'
            },
            "<CONTENT>": {
                'digit':      'digit',
                'boolean':    'boolean',
                'string':     'string',
                'list':       'list'
            },
            "<PROGRAM>": {
                'identifier': '<ATTR> <PROGRAM>',
                'while':      '<LOOP> <PROGRAM>',
                'if':         '<COND> <PROGRAM>',
                'read':       '<IO> <PROGRAM>',
                'write':      '<IO> <PROGRAM>',
                'end':        'end'
            },
            "<ATTR>": {
                'identifier': 'identifier = <EXP> ;'
            },
            "<LOOP>": {
                'while':      'while <LOGEXP> begin <PROGRAM> end ;'
            },
            "<COND>": {
                'if':         'if <LOGEXP> <PROGRAM> <COND\'>'
            },
            "<COND'>": {
                'else':       'else <PROGRAM> end',
                'end':        'end'
            },
            "<LOGEXP>": {
                'identifier': 'identifier <LOGEXP\'>'
            },
            "<LOGEXP'>": {
                'comp_op':    'comp_op identifier',
                'begin':      'ε',
                'identifier': 'ε',
                'while':      'ε',
                'if':         'ε',
                'else':       'ε',
                'read':       'ε',
                'write':      'ε',
                'logic_op':   'comp_op identifier'
            },
            "<IO>": {
                'read':       'read identifier',
                'write':      'write <CONTENT>'
            },
            "<EXP>": {
                'identifier': '<T> <E\'>',
                'digit':      '<T> <E\'>',
                'boolean':    '<T> <E\'>',
                'string':     '<T> <E\'>',
                '(':          '<T> <E\'>'
            },
            "<E'>": {
                '+':          '+ <T> <E\'>',
                '-':          '- <T> <E\'>',
                ';':          'ε',
                ')':          'ε'
            },
            "<T>": {
                'identifier': '<F> <T\'>',
                'digit':      '<F> <T\'>',
                'boolean':    '<F> <T\'>',
                'string':     '<F> <T\'>',
                '(':          '<F> <T\'>'
            },
            "<T'>": {
                '×':          '× <F> <T\'>',
                '/':          '/ <F> <T\'>',
                ';':          'ε',
                '(':          'ε',
                ')':          'ε',
                '+':          'ε',
                '-':          'ε'
            },
            "<F>": {
                'identifier': 'identifier',
                'digit':      'digit',
                'boolean':    'boolean',
                'string':     'string',
                '(':          '( <EXP> )'
            }
        }

        self.grammar = stackable_prod(master)


def stackable_prod(grm):
    """Splits the production rules in stackable pieces

    Arguments:
        grm: the grammar, with the productions in string form.

    Returns:
        The grammar with lists as productions.
    """
    for i in grm:
        for j in grm[i]:
            grm[i][j] = grm[i][j].split()
    return grm


def derive(grammar, buffer, st=['$', '<S>']):
    """
    Responsible for derivating, recursively, the buffer of words from the
    grammar, with the help of an explicit stack.

    Arguments:
        grammar: a content-free grammar in LL(1) form.
        buffer: the stream of words that will be analyzed.
        st: the stack used as a helper for the derivations. It starts with the
            end of sentence symbol and the first production of the grammar.

    Returns:
        A string that asserts the correctness of the provided source.
    """
    if not st and not buffer:
        return 'Your program matches the grammar.'

    top = st.pop()

    if {'<', '>'}.intersection(set(list(top))):
        st += grammar[top][buffer[0]][::-1]

    if buffer and buffer[0] == top:
        buffer = buffer[1:]

    return derive(grammar, buffer, st)
