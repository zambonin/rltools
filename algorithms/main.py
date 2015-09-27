from io_manager import *

aut = load('../tests/test.in')
aut.determinize()
save('../tests/afd1.out', 'automaton', aut)

r = RegularGrammar.automaton_to_grammar(aut)

save('../tests/gr1.out', 'grammar', r)

a = load('../tests/gr1.out')

b = RegularGrammar.grammar_to_automaton(a)

aut = load('../tests/test2.in')
aut.determinize()
save('../tests/afd2.out', 'automaton', aut)

aut = load('../tests/test3.in')
aut.determinize()
save('../tests/afd3.out', 'automaton', aut)
