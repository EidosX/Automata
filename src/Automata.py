from itertools import *

class Automata:
    class State:
        def __init__(self, name : str, accepting : bool = False):
            self.name = name
            self.accepting = accepting
            self.transitions = [] # Liste de tuples (symbol : str, destination : State)
        def __str__(self):
            return self.name + '*'*self.accepting + ' [' + ', '.join(map(lambda t: t[0]+'->'+t[1].name, self.transitions)) + ']'
        def getNextState(self, symbol : str):
            # Devrait tout le temps etre de longueur 1 ou 0, car l'automate est deterministe
            matchingTransitions = filter(lambda t: t[0] == symbol, self.transitions)
            for t in matchingTransitions: 
                return t[1]
    
    # transitions : [(origin : State, symbol : str, destination : State)]
    # For example:
    #   - transitions = [('1', 'b', '2'), ('2', 'b', '2')]
    #   - initialState = '1'
    #   - acceptingStates = ['1', '2']
    def __init__(self, transitions : tuple, initialState : str, acceptingStates : [str]):
        def getTransitions(state):
            for origin, symbol, destination in transitions:
                if origin == state.name: yield((symbol, next(x for x in states if x.name == destination)))

        self.initialState = None

        # On enleve les transitions epsilon inutiles d'un etat à ce meme etat
        transitions = list(filter(lambda t: not (t[1] == '%' and t[0] == t[2]), transitions))
        
        # We parse all the different states (set is very important for uniqueness!)
        statesStrings = set(chain(*map(lambda t: [t[0], t[2]], transitions)))
        
        # We convert the parsed states to State objects
        states = list(map(lambda s: Automata.State(s, s in acceptingStates), statesStrings))

        # On ajoute chaque transition à son etat d'origine
        for state in states:
            state.transitions.extend(getTransitions(state))
            if state.name == initialState: self.initialState = state
        

        if not self.isDeterministic():
            self._make_deterministic()
            if not self.isDeterministic():
                print('WARNING: Couldn\'t determinize automata')
    def deepcopy(self):
        transitions = list(chain(*map(lambda s: map(lambda t: (s.name, t[0], t[1].name), s.transitions), self.getStates())))
        initial_state = self.initialState.name
        accepting_states = list(map(lambda s: s.name, filter(lambda s: s.accepting, self.getStates())))
        return Automata(transitions, initial_state, accepting_states)

    @staticmethod
    def from_string(string : str):
        transitions = [ tuple(line.split()) for line in string.split('\n')[:-1] ]
        acceptingStates = string.split('\n')[-1][2:].split()
        return Automata(transitions, transitions[0][0], acceptingStates)
    def __str__(self):
        return '\n'.join(map(str, self.getStates()))
    
    def getStateByName(self, state_name : str):
        for state in self.getStates():
            if state.name == state_name: return state
    def getStates(self):
        states = [self.initialState]
        for state in states:
            yield state
            for sym, st in state.transitions:
                if st not in states: states.append(st)
    def normalizeNames(self):
        #On renomme les etats
        new_names = dict(zip(self.getStates(), map(str, count())))
        for state in self.getStates():
            state.name = new_names[state]


    ######################################
    #                                    #
    #            --- TP 1 ---            #
    #                                    #
    ######################################
    
    # PS: Toutes les transitions X vers X via epsilon ont été supprimées dans __init__
    def isDeterministic(self):
        for state in self.getStates():
            for key, l in groupby(sorted(map(lambda t: t[0], state.transitions))):
                if (key == '%' or len(list(l)) > 1): return False
        return True
    def isRecognized(self, word : str):
        state = self.initialState
        for symbol in word:
            if symbol == '%': continue
            if state: state = state.getNextState(symbol)
        return state != None and state.accepting

    ######################################
    #                                    #
    #            --- TP 2 ---            #
    #                                    #
    ######################################

    def _make_deterministic(self):

        # Remove epsilons

        for state in self.getStates():
            seen = []
            def get_transitions(s):
                seen.append(s)
                state.accepting = state.accepting or s.accepting
                for t in s.transitions:
                    if t[0] != '%': yield t
                    elif t[1] not in seen: yield from get_transitions(t[1])
            state.transitions = set(get_transitions(state))

        # Reduce transitions
        # On appelera un 'superetat' un ensemble / une superposition de plusieurs etats
        
        def hash_superstate(superstate):
            # We use str(hash(s)) so that we don't even need to worry about conflicting names
            return str(hash(''.join(map(lambda s: str(hash(s)), superstate))))

        states = [ set([self.initialState]) ]
        initial_state_hash = hash_superstate(states[0])
        accepting_states_hashes = []
        transitions = []

        for superstate in states:
            superstate_hash = hash_superstate(superstate)
            key = lambda t: t[0]; to_transi = lambda s: s.transitions
            reachable_states_per_symbol = groupby(sorted(chain(*map(to_transi, superstate)), key=key), key)

            # On verifie si le superetat est acceptant (si un seul de ses sous etats l'est)
            if any(map(lambda s: s.accepting, superstate)):
                accepting_states_hashes.append(superstate_hash)

            # Pour chaque superetat qu'on peut atteindre depuis l'actuel,
            # On l'ajoute à states si il n'y est pas deja
            # Puis on ajoute une transition vers le nouveau superetat
            for symbol, s in reachable_states_per_symbol:
                new_superstate = set(map(lambda s: s[1], s)); new_superstate_hash = hash_superstate(new_superstate)

                if new_superstate not in states: states.append(new_superstate)
                transitions.append((superstate_hash, symbol, new_superstate_hash))
        
        # On remplace notre automate par le nouveau
        new_automata = Automata(transitions, initial_state_hash, accepting_states_hashes)
        self.initialState = new_automata.initialState
        
        self.normalizeNames()

    ######################################
    #                                    #
    #            --- TP 3 ---            #
    #                                    #
    ######################################
    
    # Returns a new automata, doesn't change self's state
    def kleene(self): 
        automata = self.deepcopy()
        for state in filter(lambda s: s.accepting, automata.getStates()):
            state.transitions.append(('%', automata.initialState))

        new_initial_state = Automata.State(str(hash(23473842784)), True)
        new_initial_state.transitions = [('%', automata.initialState)]
        automata.initialState = new_initial_state
        
        automata._make_deterministic()
        return automata

    def concat(self, oth):
        automata = self.deepcopy()
        other = oth.deepcopy()
        # La conversion en list est très importante!
        # Sinon le generateur getStates s'adapte et renvoie les etats qu'on vient d'ajouter
        for s in list(filter(lambda s: s.accepting, automata.getStates())):
            s.transitions.append(('%', other.initialState))
            s.accepting = False
        automata._make_deterministic()
        return automata
    def union(self, oth):
        automata = self.deepcopy()
        other = oth.deepcopy()
        new_initial_state = Automata.State(str(hash(98439832)), False)
        new_initial_state.transitions = [('%', automata.initialState), ('%', other.initialState)]
        automata.initialState = new_initial_state
        automata._make_deterministic()
        print(automata)
        return automata