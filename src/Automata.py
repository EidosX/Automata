class Automata:
    class State:
        def __init__(self, number):
            self.number = number
            self.accepting = False
    class Transition:
        def __init__(self, sourceState, destState, symbol):
            self.sourceState = sourceState # State
            self.destState = destState     # State
            self.symbol = symbol           # Char
    states = []
    transitions = []
    
    def getInitialState(self):
        return self.states[0]
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