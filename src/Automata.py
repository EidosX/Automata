from itertools import *

class Automata:
    class State:
        def __init__(self, name : str, accepting : bool = False):
            self.name = name
            self.accepting = accepting
            self.transitions = [] # Liste de tuples (symbol : str, destination : State)
        def __str__(self):
            return self.name + '*' * self.accepting
        def getNextState(self, symbol : str):
            # Devrait tout le temps etre de longueur 1 ou 0, car l'automate est deterministe
            matchingTransitions = list(filter(lambda t: t[0] == symbol, self.transitions))
            for t in matchingTransitions: 
                return t[1]
    
    # transitions est un tuple de 3 (origin, symbol, destination)
    # Dans tout le reste du code, c'est un tuple de 2 (car origin est deduit de l'etat contenant)
    def __init__(self, transitions : tuple, initialState : str, acceptingStates : [str]):
        def getTransitions(state):
            for origin, symbol, destination in transitions:
                if origin == state.name: yield((symbol, self.getStateByName(destination)))

        self.states = None
        self.initialState = None

        # On enleve les transitions epsilon inutiles d'un etat à ce meme etat
        transitions = list(filter(lambda t: not (t[1] == '%' and t[0] == t[2]), transitions))

        # We parse all the different states
        statesStrings = set(chain(*map(lambda t: [t[0], t[2]], transitions)))

        # We convert the parsed states to State objects
        self.states = list(map(lambda s: Automata.State(s, s in acceptingStates), statesStrings))
        
        # On ajoute chaque transition à son etat d'origine
        for state in self.states:
            state.transitions.extend(getTransitions(state))
            if state.name == initialState: self.initialState = state

        if not self.isDeterministic():
            self._makeDeterministic()
            if not self.isDeterministic():
                print('WARNING: Couldn\'t determinize automata')
    @staticmethod
    def from_string(string : str):
        transitions = [ tuple(line.split()) for line in string.split('\n')[:-1] ]
        acceptingStates = string.split('\n')[-1][2:]
        return Automata(transitions, transitions[0][0], acceptingStates)
    
    def getStateByName(self, state_name : str):
        for state in self.states:
            if state.name == state_name: return state

    ######################################
    #                                    #
    #            --- TP 1 ---            #
    #                                    #
    ######################################
    
    def isDeterministic(self):
        # PS: Toutes les transitions X vers X via epsilon ont été supprimées dans __init__
        for state in self.states:
            for key, l in groupby(sorted(map(lambda t: t[0], state.transitions))):
                if (key == '%' or len(list(l)) > 1): return False
        return True
    def isRecognized(self, word : str):
        state = self.initialState
        for symbol in word:
            if state: state = state.getNextState(symbol)
            else: break
        return state and state.accepting

    ######################################
    #                                    #
    #            --- TP 2 ---            #
    #                                    #
    ######################################

    def _makeDeterministic(self):
        def removeEpsilons():
            def getReachableStates(state):
                for t in state.transitions:
                    if t[0] != '%': yield t
                    else: yield from getReachableStates(t[1])
            for state in self.states:  
                state.transitions = list(getReachableStates(state))
        removeEpsilons()