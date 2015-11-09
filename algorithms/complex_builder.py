#!/usr/bin/env python
# -*- coding: utf-8 -*-

from algorithms.regular_expression import RegularExpression
import string


class complex_builder(object):

    # ########## Declaration of words ##########

    words = 'else|if|while|read|write|list|bool|str|int|False|True'
    ops = '=|->|:=|and|or|not|<|>|==|>=|<=|!=|+|-|×|/'
    single_words = "{}|{}".format(words, ops)
    letters = "({})".format("|".join(string.ascii_letters))
    numbers = "|".join(string.digits)
    nonzero = "|".join(string.digits)[2:]
    underscore, quote, zero = "_", "\"", "0"
    string_char = "|".join(set(map(chr, range(32, 127))) - set("\\\"()|*"))

    # ########## Reserved words recognizer automaton ##########

    reg_exp = RegularExpression(single_words)
    aut = reg_exp.regexp_to_automaton()
    aut_2 = reg_exp.rename_aut(aut)
    aut_2.minimize()

    finals_aut = list()
    finals_aut.append(aut_2)

    # ########## Identifier recognizer automaton ##########

    list_regs = list()
    list_regs.append(letters)
    list_regs.append(numbers)
    list_regs.append(letters)
    list_regs.append(underscore)

    list_auts = list()

    for reg in list_regs:
        reg_exp = RegularExpression(reg)
        aut = reg_exp.regexp_to_automaton()
        aut.minimize()
        list_auts.append(aut)
    reg_aux = RegularExpression("")
    automatons = list()

    automatons.append(list_auts.pop(1))
    automatons.append(list_auts.pop(1))
    aut_aux = reg_aux.or_op(automatons)

    automatons = list()
    automatons.append(aut_aux)
    automatons.append(list_auts.pop(1))
    aut_aux = reg_aux.or_op(automatons)

    automatons = list()
    automatons.append(aut_aux)
    aut_aux = reg_aux.closure_op(automatons)
    list_auts.append(aut_aux)

    automatons = list()
    automatons.append(list_auts.pop(0))
    automatons.append(list_auts.pop(0))
    aut_aux = reg_aux.concat_op(automatons)
    aux_aut2 = reg_aux.rename_aut(aut_aux)
    aux_aut2.minimize()

    finals_aut.append(aux_aut2)

    # ########## Integer recognizer automaton ##########

    list_regs = list()
    list_regs.append(nonzero)
    list_regs.append(numbers)
    list_regs.append(zero)

    list_auts = list()

    for reg in list_regs:
        reg_exp = RegularExpression(reg)
        aut = reg_exp.regexp_to_automaton()
        aut.minimize()
        list_auts.append(aut)
    reg_aux = RegularExpression("")

    automatons = list()
    automatons.append(list_auts.pop(1))
    aux_aut = reg_aux.closure_op(automatons)
    list_auts.insert(1, aux_aut)

    automatons = list()
    automatons.append(list_auts.pop(0))
    automatons.append(list_auts.pop(0))
    aux_aut = reg_aux.concat_op(automatons)
    list_auts.insert(1, aux_aut)

    aux_aut = reg_aux.or_op(list_auts)
    aux_aut2 = reg_aux.rename_aut(aux_aut)
    aux_aut2.minimize()

    finals_aut.append(aux_aut2)

    # ########## String recognizer automaton ##########

    list_regs = list()
    list_regs.append(quote)
    list_regs.append(string_char)
    list_regs.append(quote)

    list_auts = list()

    for reg in list_regs:
        reg_exp = RegularExpression(reg)
        aut = reg_exp.regexp_to_automaton()
        aut.minimize()
        list_auts.append(aut)
    reg_aux = RegularExpression("")

    automatons = list()
    automatons.append(list_auts.pop(1))
    aux_aut = reg_aux.closure_op(automatons)
    list_auts.insert(1, aux_aut)

    automatons = list()
    automatons.append(list_auts.pop(0))
    automatons.append(list_auts.pop(0))
    aux_aut = reg_aux.concat_op(automatons)
    list_auts.insert(0, aux_aut)

    aux_aut = reg_aux.concat_op(list_auts)
    aux_aut2 = reg_aux.rename_aut(aux_aut)
    aux_aut2.minimize()

    finals_aut.append(aux_aut2)

    # ########## Union of the automata created above ##########

    automatons = list()
    while len(finals_aut) > 1:
        automatons.append(finals_aut.pop(0))
        automatons.append(finals_aut.pop(0))
        aut = reg_aux.or_op(automatons)
        aut2 = reg_aux.rename_aut(aut)
        finals_aut.append(aut2)
        automatons = list()

    _aut = finals_aut.pop(0)
    _aut.determinize()
    final_aut = _aut
