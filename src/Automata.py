class Automata:
    class State:
        def __init__(self, number):
            self.number = number
            self.accepting = False
    class Transition:
        def __init__(self, sourceState, destState, symbol):
            self.sourceState = sourceState # Int
            self.destState = destState     # Int
            self.symbol = symbol           # Char
    states = []         # [Int]
    transitions = []    # [Transition]
    
    def __init__(self, sourceTxt):
        lines = sourceTxt.split('\n')
        # We parse each line defining a transition
        # le [:-2] retire la derniere ligne (vide) et la ligne definissant les transitions
        for words in map(lambda l: l.split(' '), lines[:-2]):
            # We parse the content of the line
            sourceState = int(words[0])
            destState   = int(words[2])
            symbol      = words[1]
            # We add the two states if they're not already in the list
            if list(map(lambda s: s.number, self.states)).count(sourceState) == 0:
                self.states.append(Automata.State(sourceState))
            if list(map(lambda s: s.number, self.states)).count(destState) == 0:
                self.states.append(Automata.State(destState))
            # We add the transition in the list
            self.transitions.append(Automata.Transition(sourceState, destState, symbol))
        # We parse the last line i.e the accepting states
        acceptingStates = lines[-2].split(' ')[+1:]
        for state in self.states:
            for accepting in acceptingStates:
                if state.number == int(accepting):
                    state.accepting = True

    def getInitialState(self):
        return self.states[0]
    # Returns all transitions which starting state is 'state'
    def getTransitions(self, state):
        return list(filter(lambda t: t.sourceState == state.number, self.transitions))
    def getAlphabet(self):
        alphabet = []
        for transition in self.transitions:
            if alphabet.count(transition.symbol) == 0:
                alphabet.append(transition.symbol)
        return alphabet


    def isDeterministic(self):
        for state in self.states:
            # On fait une liste de toutes les transitions partant de l'etat state
            outTransitions = self.getTransitions(state)
            outSymbols = list(map(lambda t: t.symbol, outTransitions))

            # On verifie qu'il n'y ait pas d'epsilon transition autre que la transition sur soi meme
            if list(filter(lambda t: t.symbol == '%' and t.sourceState != t.destState, outTransitions)) != []:
                return False

            # On verifie qu'il n'y a pas de duplicats
            if len(set(outSymbols)) != len(outSymbols):
                return False
        return True
    def isAccepted(self, str):
        currentState = self.getInitialState()
        for char in str:
            # On fait une liste des transitions possibles depuis currentState avec le symbole char.
            # Si l'automate est deterministe cette liste contient soit 0 soit 1 elements
            transitions = list(filter(lambda t: t.symbol == char, self.getTransitions(currentState)))
            # Si l'etat n'a pas de transition pour la lettre alors le mot n'est pas reconnu
            if (len(transitions) == 0):
                return False
            # Sinon on met a jour currentState.
            # Notons qu'on prend simplement le premier element de transitions,
            # car on suppose que l'automate est deterministe.
            # Sinon il faudrait implementer un algorithme recursif.
            currentState = list(filter(lambda s: s.number == transitions[0].destState, self.states))[0]
        return True