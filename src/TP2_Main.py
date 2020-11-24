from Automata import *

def removeEpsilons(automata):
    # Format: [(nextState : State, symbol : String)]
    def getPossibleNextStates(state):
        nextStates = []
        for transition in automata.getTransitions(state):
            dest = automata.getStateByName(transition.destState)
            if (transition.symbol == '%'):
                ns = getPossibleNextStates(dest)
                nextStates.extend(ns)
            else:
                nextStates.append((dest, transition.symbol))
        return nextStates
    def isAccepting(state):
        if state.accepting:
            return True
        for transition in automata.getTransitions(state):
            if (transition.symbol == '%'):
                return isAccepting(automata.getStateByName(transition.destState))
        return False

    states = []
    transitions = []
    for state in automata.states:
        ss = Automata.State(state.name); ss.accepting = isAccepting(state)
        states.append(ss)
        nextStates = getPossibleNextStates(state)
        transitions.extend(list(map(lambda ds: Automata.Transition(ss.name,ds[0].name, ds[1]), nextStates)))
    return Automata(states, transitions)


source = """0 % 1
0 % 2
1 a 1
2 b 2
A 1 2"""

automata = fileToAutomata(source)
automata = removeEpsilons(automata)
for s in automata.states:
    print(s.toString())

