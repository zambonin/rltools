#!/usr/bin/env python
# -*- coding: utf-8 -*-

from algorithms.regular_expression import RegularExpression
from algorithms.tokenizer import Tokenizer
from pprint import pprint

class complex_builder():
    simple_identifier = '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)'
    numbers = '0|1|2|3|4|5|6|7|8|9'
    nonzero_num = '1|2|3|4|5|6|7|8|9'
    underscore = '_'
    quote = '"'
    string = " |!|#|$|%|&|'|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|}|~"


    list_regs = list()
    list_regs.append(simple_identifier)
    list_regs.append(numbers)
    list_regs.append(simple_identifier)
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
    #aut_aux2 = reg_aux.rename_aut(aut_aux)

    automatons = list()
    automatons.append(aut_aux)
    automatons.append(list_auts.pop(1))
    aut_aux = reg_aux.or_op(automatons)
    #aut_aux2 = reg_aux.rename_aut(aut_aux)

    automatons = list()
    automatons.append(aut_aux)
    aut_aux = reg_aux.closure_op(automatons)
    #aux_aux2 = reg_aux.rename_aut(aut_aux)
    list_auts.append(aut_aux)

    automatons = list()
    automatons.append(list_auts.pop(0))
    automatons.append(list_auts.pop(0))
    aut_aux = reg_aux.concat_op(automatons)
    aux_aut2 = reg_aux.rename_aut(aut_aux)
    aux_aut2.minimize()

    finals_aut = list()
    finals_aut.append(aux_aut2)

    #STARTING THE INTEGER AUTOMATON-----------------------------------------|

    list_regs = list()
    list_regs.append(nonzero_num)
    list_regs.append(numbers)
    list_regs.append('0')

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


    #STARTING THE STRING AUTOMATON--------------------------------------|
    list_regs = list()
    list_regs.append(quote)
    list_regs.append(string)
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

def test():
   c = complex_builder()
test()
