#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""regular_expression.py

Definition of a regular expression and its conversion from and to finite
automata, through generalized nondeterministic finite automaton (GNFA) and
Thompson's construction algorithms, respectively.

Gustavo Zambonin & Matheus Ben-Hur de Melo Leite, UFSC, October 2015.
"""

from algorithms.finite_automaton import FiniteAutomaton


class RegularExpression(object):
    """A regular expression is a sequence of characters that define a search
    pattern. It consists of constants (the alphabet or the empty string,
    generally ε) and operator symbols that act upon these constants and sets
    made of them. The operations are described as follows:
        * concatenation of strings, i.e., {'a'}{'b'} = {'ab'};
        * union or alternation of strings (|), i.e. {'a'} | {'b'} = {'a', 'b'}.
          Other operators such as + can be used instead of the vertical bar;
        * the Kleene star operation (*), that returns the set of all strings
          produced by concatenating any finite non-negative number of strings
          from another given set, i.e. {'a'} = {ε, 'a', 'aa', 'aaa', ...}.
    Parentheses can be used to denote the operations' application range, but if
    omitted, Kleene star has priority over concatenation that has priority
    over alternation.

    Attributes:
        expression: the string for the regular expression.
        alphabet: all symbols that are not operators or parentheses compose
            the alphabet.
    """

    def __init__(self, expression):
        """Inits RegularGrammar with the attributes introduced above.

        Raises:
            ValueError: when unknown operators are added to the expression.
        """
        self.expression = expression
        valid_symbols = set(map(chr, range(32, 127))) - set("\\()|*") | {'×'}

        self.alphabet = {i for i in expression if i in valid_symbols}
        valid_chars = set("()|*") | self.alphabet
        if set(expression) - valid_chars:
            raise ValueError

    def diff_aut(self, automaton, suffix):
        """Renames the automaton's states.

        Attributes:
            automaton: the automaton to be manipulated.
            suffix: the chosen string to be added to the states.

        Returns:
            An automaton with different names for states.
        """
        aux_aut = FiniteAutomaton({state+suffix for state in automaton.states},
                                  automaton.alphabet, {},
                                  automaton.init_state + suffix,
                                  {frozenset([set(state).pop() + suffix])
                                      for state in automaton.final_states})

        for state in automaton.transitions:
            key = frozenset([set(state).pop() + suffix])
            aux_aut.transitions[key] = {}
            for symbol in automaton.transitions[state]:
                aux_aut.transitions[key][symbol] = set()
                for element in automaton.transitions[state][symbol]:
                    if isinstance(element, str):
                        element = [element]
                    aux_aut.transitions[key][symbol].add(
                        frozenset([set(element).pop() + suffix]))

        return aux_aut

    def add_transitions(self, automaton):
        """Fills the missing transitions on an automaton.

        Attributes:
            automaton: the automaton to be manipulated.

        Returns:
            A new automaton with all possible transitions mapped.
        """
        for letter in automaton.alphabet:
            for state in automaton.transitions:
                try:
                    automaton.transitions[state][letter]
                except KeyError:
                    automaton.transitions[state][letter] = {}
                    automaton.transitions[state][letter] = set()

        return automaton

    def or_op(self, automatons):
        """Implements the regular expression alternation operator.

        Attributes:
            automatons: a list of two automatons to be merged.

        Returns:
            A single automaton that accepts either language its parts accepted.
        """
        aut1 = self.diff_aut(automatons[0], "%")
        aut2 = self.diff_aut(automatons[1], "&")
        or_aut = FiniteAutomaton({"initOr"}, set(), {
            frozenset(["initOr"]): {
                aut1.epsilon: set()
            }
            }, "initOr", set())

        for each in [aut1, aut2]:
            or_aut.states |= each.states
            or_aut.alphabet |= each.alphabet
            or_aut.transitions.update(each.transitions)
            or_aut.transitions[frozenset(["initOr"])][or_aut.epsilon].add(
                each.init_state)
            or_aut.final_states |= each.final_states

        return self.add_transitions(or_aut)

    def concat_op(self, automatons):
        """Implements the regular expression concatenation operator.

        Attributes:
            automatons: a list of two automatons to be merged.

        Returns:
            An automaton that accepts words starting with the first automaton
            language and ending with the last automaton language.
        """
        aut1 = self.diff_aut(automatons[0], "#")
        aut2 = self.diff_aut(automatons[1], "$")
        concat_aut = FiniteAutomaton(aut1.states | aut2.states,
                                     aut1.alphabet | aut2.alphabet, {},
                                     aut1.init_state, aut2.final_states)
        concat_aut.transitions.update(aut1.transitions)
        concat_aut.transitions.update(aut2.transitions)

        for state in aut1.final_states:
            try:
                concat_aut.transitions[state][concat_aut.epsilon].add(
                    frozenset([aut2.init_state]))
            except KeyError:
                concat_aut.transitions[state][concat_aut.epsilon] = set()
                concat_aut.transitions[state][concat_aut.epsilon].add(
                    frozenset([aut2.init_state]))

        return self.add_transitions(concat_aut)

    def closure_op(self, automatons):
        """Implements the regular expression Kleene star operator.

        Attributes:
            automatons: a list of automatons to be operated on.

        Returns:
            An automaton that will accept any non-negative number of
            repetitions of its original language.
        """
        clsr_aut = FiniteAutomaton(
            {"initClsr"}, set(), {
                frozenset(["initClsr"]): {
                    automatons[0].epsilon: set()
                }
                }, "initClsr", {frozenset(["initClsr"])})

        e = clsr_aut.epsilon
        for each in automatons:
            clsr_aut.states |= each.states
            clsr_aut.alphabet |= each.alphabet
            clsr_aut.transitions[frozenset(["initClsr"])][e].add(
                frozenset([each.init_state]))
            clsr_aut.transitions.update(each.transitions)
            clsr_aut.final_states |= each.final_states
            for state in each.final_states:
                try:
                    clsr_aut.transitions[state][e] = set()
                except KeyError:
                    clsr_aut.transitions[state] = {}
                    clsr_aut.transitions[state][e] = set()
                clsr_aut.transitions[state][e].add(frozenset(["initClsr"]))

        return self.add_transitions(clsr_aut)

    def single_state(self, transition):
        """Implements the most basic type of automaton.

        Attributes:
            transition: the only transition made on the automaton, represented
            by a set of symbols.

        Returns:
            An automaton that accepts only one set of symbols.
        """
        single_aut = FiniteAutomaton({"q0" + transition, "q1" + transition},
                                     {transition}, {
                                     frozenset(["q0"+transition]): {
                                         transition: {
                                             frozenset(["q1"+transition])
                                         }
                                     }, frozenset(["q1"+transition]): {}},
                                     "q0" + transition,
                                     {frozenset(["q1"+transition])})
        return self.add_transitions(single_aut)

    def empty_word(self):
        """Implements the automaton that accepts the empty word.

        Returns:
            A basic automaton with just one state and no transitions.
        """
        return FiniteAutomaton({"q0"}, set(), {}, "q0", {"q0"})

    def analyse_expression(self, expression):
        """Reads and consumes the given expression, organizing it into a list.

        Attributes:
            expression: the regular expression in form of a string.

        Returns:
            A list with a special notation denoting the order and priority of
            the operators and symbols.
        """
        separator = "ε"
        i = 0
        _list = []
        while len(expression) != 0:
            if expression[i] in self.alphabet:
                _list.append(expression[i])
                expression = expression[:i] + expression[i+1:]
            elif expression[i] == "|":
                _list.append(separator)
                _next = expression[i+1]
                if _next == "(":
                    aux = 2
                    while _next != ")":
                        _next = expression[i+aux]
                        if _next != ")":
                            _list.append(_next)
                        aux += 1
                    expression = expression[:i] + expression[i+aux:]
                elif _next in self.alphabet:
                    try:
                        after_next = expression[i+2]
                    except IndexError:
                        after_next = ""
                    it_num = 3
                    nexts = list()
                    while after_next in self.alphabet:
                        nexts.append(after_next)
                        try:
                            after_next = expression[i+it_num]
                        except IndexError:
                            it_num += 1
                            break
                        it_num += 1
                    _list.append(_next)
                    _list.extend(nexts)
                    if after_next == "*":
                        _list.append(after_next)
                        it_num +=1
                    expression = expression[:i] + expression[i+(it_num-1):]
                _list.append("|")
            elif expression[i] in ["(", ")", "*"]:
                if expression[i] == "*":
                    _list.append("*")
                if expression[i] == "(":
                    _list.append(separator)
                expression = expression[:i] + expression[i+1:]

        return _list

    def execute_operations(self, list):
        """Assembles automata according to operators and symbols. It is a
        representation of Thompson's construction algorithm idea: construct
        basic automata and apply operations to them, the final product
        getting more complex over every iteration of the list.

        Attributes:
            a list of symbols and operators with a respective order.

        Returns:
            The final automaton for a given regular expression.
        """
        partial_auts = []
        while len(list) != 0:
            char = list.pop(0)
            if char == "ε":
                aux_lst = []
                _next = list.pop(0)
                while _next in self.alphabet:
                    aux_lst.append(self.single_state(_next))
                    _next = list.pop(0)
                    if _next == "*":
                        aut = [aux_lst.pop()]
                        aux_lst.append(self.closure_op(aut))
                    if len(aux_lst) == 2:
                        param_list = [aux_lst.pop(0)]
                        param_list.append(aux_lst.pop(0))
                        aux_lst.append(self.concat_op(param_list))

                if len(partial_auts) == 2:
                    aux_list = [partial_auts.pop(0)]
                    aux_list.append(partial_auts.pop(0))
                    partial_auts.append(self.concat_op(aux_list))
                partial_auts.extend(aux_lst)
                if _next != "*":
                    list.insert(0, _next)
            if char in self.alphabet:
                if len(partial_auts) == 2:
                    aux_list = [partial_auts.pop(0)]
                    aux_list.append(partial_auts.pop(0))
                    partial_auts.append(self.concat_op(aux_list))
                partial_auts.append(self.single_state(char))
            if char == "|":
                if len(partial_auts) == 3:
                    aux_list = [partial_auts.pop(1)]
                    aux_list.append(partial_auts.pop())
                    partial_auts.append(self.concat_op(aux_list))
                partial_auts = [self.or_op(partial_auts)]
            if char == "*":
                aut = [partial_auts.pop()]
                partial_auts.append(self.closure_op(aut))

        if len(partial_auts) == 2:
            return self.add_transitions(self.concat_op(partial_auts))
        return self.add_transitions(partial_auts.pop())

    def rename_aut(self, automaton):
        """Makes the automaton's states' names readable.

        Attributes:
            automaton: the automaton with confusing names.

        Returns:
            An automaton with normal names for states.
        """

        new_aut = FiniteAutomaton(set(), automaton.alphabet, {}, "", set())

        new_states = {}
        for i, j in zip(automaton.states, range(len(automaton.states))):
            new_states[i] = 'q' + str(j)

        for i in new_states:
            state = new_states[i]
            new_aut.states.add(state)
            if frozenset([i]) in automaton.final_states:
                final_state = set([new_states[i]])
                new_aut.final_states.add(frozenset(final_state))
            if i == automaton.init_state:
                new_aut.init_state = new_states[i]

        for i in automaton.transitions:
            new_key = frozenset([new_states[list(set(i))[0]]])
            new_aut.transitions[new_key] = {}
            for j in automaton.transitions[i]:
                #new_aut.transitions[new_key][j] = automaton.transitions[i][j]
                new_aut.transitions[new_key][j] = set()
                for k in automaton.transitions[i][j]:
                    if isinstance(k, frozenset):
                        if len(k) > 1:
                            to_these_states = {new_states[i] for i in automaton.transitions[i][j]}
                            new_aut.transitions[new_key][j] |= to_these_states
                        else:
                            to_this_state = set([new_states[list(set(k))[0]]])
                            new_aut.transitions[new_key][j] |= to_this_state
                    else:
                            to_this_state = set([new_states[k]])
                            new_aut.transitions[new_key][j] |= to_this_state


        return new_aut

    def regexp_to_automaton(self):
        """Calls the right methods in the right order."""
        final = self.execute_operations(
            self.analyse_expression(self.expression))
        return self.rename_aut(final)

    def automaton_to_regexp(automaton):
        """Converts a finite automaton into a vanilla, non-reduced regular
        expression. It is an implementation of the generalized nondeterministic
        finite automaton algorithm. The general idea will be described below:
          * add new initial state with epsilon-moves to the old initial state;
          * add new final state with epsilon-moves from the old final states;
          * remove one state at a time, except the ones just added, recomputing
          all transitions that pass through that state;
          * end the process when the only remaining states are the ones added.

        Attributes:
            automaton: the automaton to be consumed and converted.

        Returns:
            The transition from the new initial to the new final states will
            consist of the regular expression equivalent to the original
            automaton.
        """
        transitions = automaton.transitions
        states = {'i', 'f', frozenset()} | automaton.states
        init_state = automaton.init_state
        final_states = [set(x) for x in automaton.final_states]

        expr = {}
        for x in states:
            for y in states:
                expr[x, y] = None

        expr['i', frozenset(init_state)] = automaton.epsilon
        for x in final_states:
            expr[frozenset(x), 'f'] = automaton.epsilon

        old_transitions = transitions.copy()
        transitions.clear()

        for i in old_transitions:
            transitions[frozenset(list(i)[0].split(','))] = old_transitions[i]

        for x in transitions:
            for t in transitions[x]:
                expr[x, frozenset(transitions[x][t])] = t

        while len(states) > 2:
            s = next(x for x in states if isinstance(x, frozenset))
            for x in states:
                for y in states:
                    if (expr[x, s] is not None and expr[s, y] is not None and
                       x != s and y != s):
                        l1 = expr[x, s]
                        l2 = expr[s, s]
                        l3 = expr[s, y]
                        l4 = expr[x, y]

                        if l2 is None and l4 is None:
                            part_re = "(%s)(%s)" % (l1, l3)
                        elif l2 is not None and l4 is not None:
                            part_re = "((%s)(%s)*(%s))|%s" % (l1, l2, l3, l4)
                        elif l2 is None and l4 is not None:
                            part_re = "(%s)(%s)|%s" % (l1, l3, l4)
                        elif l4 is None and l2 is not None:
                            part_re = "(%s)(%s)*(%s)" % (l1, l2, l3)

                        expr[x, y] = part_re
            states.remove(s)

        return expr['i', 'f']