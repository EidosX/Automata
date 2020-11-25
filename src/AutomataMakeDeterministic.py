from Automata import *
from Tools.GroupBy import *

# Prends un automate en entrée et renvoie un automate determiste equivalent
def makeDeterministic(automata):
    # Format: [(nextState : State, symbol : String)]
    def getPossibleNextStates(automata, state):
        nextStates = []
        for transition in automata.getTransitions(state):
            dest = automata.getStateByName(transition.destState)
            if (transition.symbol == '%'):
                ns = getPossibleNextStates(automata, dest)
                nextStates.extend(ns)
            else:
                nextStates.append((dest, transition.symbol))
        return nextStates

    # Returns a new automata which is equivalent to 'automata' but with no epsilon transition
    def removeEpsilons(automata):
        # Returns true if state is accepting or if it leads to an accepting state through epsilon transitions
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
            nextStates = getPossibleNextStates(automata, state)
            transitions.extend(list(map(lambda ds: Automata.Transition(ss.name,ds[0].name, ds[1]), nextStates)))
        return Automata(states, transitions)

    # Returns a new automata equivalent to 'automata' but with less than 2 transition per symbol on each state.
    # The input automata must not have any epsilon transition.
    def reduceTransitions(automata):
        def hashStates(stateList):
            str = ""
            for s in set(stateList):
                str += s.name + "__"
            return str
        newStates = [ [automata.getInitialState()] ]
        newTransitions = []
        for S in newStates:
            nextTransitions = sum(map(lambda s: getPossibleNextStates(automata, s), S), []) # sum [] applatit la liste
            # par exemple {'a': [state1], 'b': [state1, state2]}
            dictionnary = groupBy(lambda t: t[1], lambda t: t[0], nextTransitions)
            for (k, v) in dictionnary.items():
                newTransitions.append(hashStates(S) + " " + k + " " + hashStates(v))
                if hashStates(v) not in map(hashStates, newStates):
                    newStates.append(v)
        # Maintenant on trouve les etats acceptants
        acceptingStates = 'A '
        for s in newStates:
            if any(map(lambda x: x.accepting, s)):
                acceptingStates += hashStates(s) + " "
        return textToAutomata('\n'.join(newTransitions) + '\n' + acceptingStates)

    return reduceTransitions(removeEpsilons(automata))
    
