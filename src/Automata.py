from itertools import *

class Automata:
    class State:
        def __init__(self, name : str, accepting : bool = False):
            self.name = name
            self.accepting = accepting
            self.transitions = [] # Liste de tuples (symbol : str, destination : State)
        def __str__(self):
            return self.name + '*'*self.accepting
    
    # transitions est un tuple de 3 (origin, symbol, destination)
    # Dans tout le reste du code, c'est un tuple de 2 (car origin est deduit de l'etat contenant)
    def __init__(self, transitions, acceptingStates : [str]):
        def getTransitions(state):
            for origin, symbol, destination in transitions:
                if origin == state.name:  
                    yield((symbol, destination))

        # We parse all the different states
        statesStrings = set(chain(*map(lambda t: [t[0], t[2]], transitions)))

        # We convert the parsed states to State objects
        self.states = list(map(lambda s: Automata.State(s, s in acceptingStates), statesStrings))
        
        # On ajoute chaque transition à son etat d'origine
        for state in self.states:
            state.transitions.extend(getTransitions(state))
    @staticmethod
    def from_string(string : str):
        transitions = [ tuple(line.split()) for line in string.split('\n')[:-1] ]
        acceptingStates = string.split('\n')[-1][2:]
        return Automata(transitions, acceptingStates)

    ######################################
    #                                    #
    #                TP 1                #
    #                                    #
    ######################################
    
