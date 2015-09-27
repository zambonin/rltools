from pprint import pprint
from notamotua import Automaton

class Regular_grammar:
    def __init__(self, automaton):
        self.productions = {}
        self.automaton = automaton
        self.terminals = set()
        self.non_terminals = set()
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
            terminals = terminals[:-1]

        non_terminals = "Non-terminals: "

        for non_terminal in self.non_terminals:
            non_terminals += non_terminal+", "
        if non_terminals.endswith(", "):
            non_terminals = non_terminals[:-1]

        initial_prodction = "Initital Production: "+self.init_production

        return terminals+"\n"+non_terminals+"\n"+initial_prodction+"\n"+grammar


    def automaton_to_grammar(self):
        self.non_terminals.update(self.automaton.alphabet)
        init_prod = ""
        for part in self.automaton.init_state:
            init_prod += part.upper()
        self.init_production = init_prod
        for state in self.automaton.transitions: #each state of the automaton
            terminal = ""
            for part in state:
                terminal += part.upper()
            self.productions[terminal] = set()
            self.terminals.add(terminal)
            for letter in self.automaton.transitions[state]: #each letter of the alphabet
                aux = ""
                for i in self.automaton.transitions[state][letter]:
                    aux += i.upper()
                if aux != "":
                    self.productions[terminal].add(letter+aux)
                if self.automaton.transitions[state][letter] in self.automaton.final_states:
                    self.productions[terminal].add(letter)


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
    """print("Transitions")
    pprint(b.transitions)
    print("Initial :",b.init_state)
    print("States")
    pprint(b.states)
    print("Finals")
    pprint(b.final_states)"""

    r = Regular_grammar(b)
    r.automaton_to_grammar()
    print(r)
test()

