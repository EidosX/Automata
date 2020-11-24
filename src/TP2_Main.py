from Automata import *

def removeEpsilons(automata):
    # Format: (nextState, symbol)
    def getPossibleNextStates(state):
        nextStates = []
        for transition in automata.getTransitions(state):
            dest = automata.getStateByName(transition.destState)
            if (transition.symbol == '%'):
                d = 0
                nextStates.extend(getPossibleNextStates(dest))
            else:
                nextStates.append((dest, transition.symbol))
        return nextStates
    states = []
    transitions = []
    for state in automata.states:
        ss = Automata.State(state.name); ss.accepting = state.accepting
        states.append(ss)
        nextStates = getPossibleNextStates(state)
        transitions.extend(list(map(lambda ds: Automata.Transition(ss.name,ds[0].name, ds[1]), nextStates)))
    return Automata(states, transitions)


source = """1 1 2
2 1 3
3 1 4
4 0 4
4 1 4
2 0 5
2 1 5
5 0 6
5 1 6
6 0 4
6 1 4
A 4"""

automata = fileToAutomata(source)
removeEpsilons(automata)