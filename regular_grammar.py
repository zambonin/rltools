from pprint import pprint
from notamotua import Automaton


class RegularGrammar:
    def __init__(self, productions, terminals, non_terminals, init_production):
        self.productions = {}
        self.terminals = set()
        self.non_terminals = set()
        self.init_production = init_production

    def __str__(self):
        grammar = ""
        for production in self.productions:
            grammar += "["+production+"]"+" ->"
            for part in self.productions[production]:
                grammar += " "+part+" |"
            if grammar.endswith("|"):
                grammar = grammar[:-1]
            grammar+= "\n"

        terminals = "Terminals: "

        for terminal in self.terminals:
            terminals += terminal+", "
        if terminals.endswith(", "):
            terminals = terminals[:-2]

        non_terminals = "Non-terminals: "

        for non_terminal in self.non_terminals:
            non_terminals += non_terminal+", "
        if non_terminals.endswith(", "):
            non_terminals = non_terminals[:-2]

        initial_prodction = "Initital Production: "+self.init_production

        return terminals+"\n"+non_terminals+"\n"+initial_prodction+"\n"+grammar

    def automaton_to_grammar(self, automaton):
        self.non_terminals.update(automaton.alphabet)
        init_prod = ""
        for part in automaton.init_state:
            init_prod += part.upper()
        self.init_production = init_prod
        for state in automaton.transitions: #each state of the automaton
            terminal = ""
            for part in state:
                terminal += part.upper()
            self.productions[terminal] = set()
            self.terminals.add(terminal)
            for letter in automaton.transitions[state]: #each letter of the alphabet
                aux = ""
                for i in automaton.transitions[state][letter]:
                    aux += i.upper()
                if aux != "":
                    self.productions[terminal].add(letter+aux)
                if automaton.transitions[state][letter] in automaton.final_states:
                    self.productions[terminal].add(letter)

    def grammar_to_automaton(self):
        states = set()
        transitions = {}
        final_states = set()
        initial_state = self.init_production.lower()
        alphabet = self.non_terminals
        for production in self.productions:
            states.add(production.lower())
            transitions[frozenset([production.lower()])] ={}
            for part in self.productions[production]:
                if len(part) > 1:
                    transitions[frozenset([production.lower()])][part[0]] = part[1:].lower()

            for part in self.productions[production]: #putting the final states
                if len(part) == 1:
                    final_states.add(frozenset([transitions[frozenset([production.lower()])][part]]))
        if len(self.productions[production]) == 0:
            for symbol in alphabet:
                transitions[frozenset([production.lower()])][symbol] = set()

        automaton = Automaton()
        automaton.alphabet = alphabet
        automaton.transitions = transitions
        automaton.final_states = final_states
        automaton.init_state = initial_state
        automaton.states = states
        return automaton





def test():

    b = Automaton()
    b.states.add("p")
    b.states.add("q")
    b.states.add("r")
    b.states.add("s")

    b.init_state = "p"
    b.final_states.add(frozenset("r"))

    b.transitions[frozenset(["p"])] = {}
    b.transitions[frozenset(["p"])]["λ"] = {"p","q"}
    b.transitions[frozenset(["p"])]["a"] = set()
    b.transitions[frozenset(["p"])]["b"] = {"q"}
    b.transitions[frozenset(["p"])]["c"] = {"r"}

    b.transitions[frozenset(["q"])] = {}
    b.transitions[frozenset(["q"])]["a"] = {"p"}
    b.transitions[frozenset(["q"])]["b"] = {"r"}
    b.transitions[frozenset(["q"])]["c"] = {"p","q"}

    b.transitions[frozenset(["r"])] = {}
    b.transitions[frozenset(["r"])]["a"] = set()
    b.transitions[frozenset(["r"])]["b"] = set()
    b.transitions[frozenset(["r"])]["c"] = set()

    b.alphabet.add("a")
    b.alphabet.add("b")
    b.alphabet.add("c")
    b.determinization()

    r = RegularGrammar({}, set(), set(), "")
    r.automaton_to_grammar(b)
    print(r)
    e = r.grammar_to_automaton()


    a = Automaton()
    a.states.add("q0")
    a.states.add("q1")
    a.states.add("q2")
    a.states.add("q3")

    a.init_state = "q0"
    a.final_states.add(frozenset(["q3"]))

    q0 = frozenset(["q0"])
    a.transitions[q0] = {}
    a.transitions[q0]["a"] = {"q0", "q1"}
    a.transitions[q0]["b"] = {"q0"}

    a.transitions[frozenset(["q1"])] = {}
    a.transitions[frozenset(["q1"])]["a"] = {"q2"}
    a.transitions[frozenset(["q1"])]["b"] = set()

    a.transitions[frozenset(["q2"])] = {}
    a.transitions[frozenset(["q2"])]["a"] = set()
    a.transitions[frozenset(["q2"])]["b"] = {"q3"}

    a.transitions[frozenset(["q3"])] = {}
    a.transitions[frozenset(["q3"])]["a"] = {"q3"}
    a.transitions[frozenset(["q3"])]["b"] = {"q3"}


    a.alphabet.add("a")
    a.alphabet.add("b")
    a.determinization()

    r = RegularGrammar({}, set(), set(), "")
    r.automaton_to_grammar(a)
    print(r)
    d = r.grammar_to_automaton()

test()

