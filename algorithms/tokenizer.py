#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tokenizer.py

A simple text segmentation utility for the lexical analysis part of a compiler.

Gustavo Zambonin & Matheus Ben-Hur de Melo Leite, UFSC, November 2015.
"""


class Tokenizer(object):
    """A tokenizer performs lexical analysis by going through every character
    of an input string (the source code desired to be proof-read) and matching
    it with words accepted by a finite automaton.

    Attributes:
        automaton: the means by which the words are computed.
        input_file: a text file with source code for the language.
    """

    def __init__(self, automaton, input_file):
        """Inits Tokenizer with the attributes introduced above."""
        self.automaton = automaton
        self.input_file = input_file

    def analyze(self):
        """Reads lexemes from a file and transforms them in tokens.

        Returns:
            A tuple consisting of the tokens (which themselves are tuples
            containing the lexeme and its classification within the lexical
            structure) and a list of words that could not be understood by
            the automaton. along with their placement on the source file.
        """
        with open(self.input_file, 'r') as file:
            tokens, errors, separators = [], [], ["\n", " "]
            line_number = 0

            if isinstance(self.automaton.init_state, str):
                reset = frozenset([self.automaton.init_state])
            else:
                reset = frozenset(self.automaton.init_state)

            while True:
                line = file.readline()
                if not line:
                    break
                line_number += 1
                curr_state, word = reset, ""
                for letter in line:
                    if ((curr_state == frozenset() or curr_state == set())
                       and letter not in separators):
                        word += str(letter)
                    elif letter in separators:
                        if curr_state in self.automaton.final_states:
                            aux = "".join(p for p in set(curr_state))
                            tokens.append((word, aux))
                        elif word:
                            errors.append("{}:{} '{}' not recognized".format(
                                          self.input_file, line_number, word))
                        curr_state = reset
                        word = ""
                    else:
                        word += str(letter)
                        try:
                            curr_state = frozenset(
                                self.automaton.transitions[curr_state][letter])
                        except KeyError:
                            curr_state = set()

        return tokens, errors
