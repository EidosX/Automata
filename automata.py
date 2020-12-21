from itertools import groupby, chain, count

class Automata:
    class State:
        def __init__(self, name: str, accepting: bool = False):
            self.name = name
            self.accepting = accepting
            self.transitions = [] # Liste de tuples (symbol: str, destination: State)
        def __str__(self):
            transitions_str = f" [{', '.join(t[0]+'->'+t[1].name for t in self.transitions)}]"
            return self.name + '*'*self.accepting + transitions_str
        def get_next_state(self, symbol: str):
            # Devrait tout le temps etre de longueur 1 ou 0, car l'automate est deterministe
            matching_transitions = [t for t in self.transitions if t[0] == symbol]
            return matching_transitions[0][1] if matching_transitions else None

    # transitions: [(origin: State, symbol: str, destination: State)]
    # For example:
    #   - transitions = [('1', 'b', '2'), ('2', 'b', '2')]
    #   - initial_state = '1'
    #   - acceptingStates = ['1', '2']
    def __init__(self, transitions: [tuple], initial_state: str, acceptingStates: [str]):
        def get_transition(state):
            for origin, symbol, destination in transitions:
                if origin == state.name:
                    yield(symbol, next(x for x in states if x.name == destination))
        self.initial_state = None

        # On enleve les transitions epsilon inutiles d'un etat à ce meme etat
        transitions = list(filter(lambda t: not (t[1] == '%' and t[0] == t[2]), transitions))

        # We parse all the different states (set is very important for uniqueness!)
        states_strings = set(chain(*map(lambda t: [t[0], t[2]], transitions)))

        # We convert the parsed states to State objects
        states = list(map(lambda s: Automata.State(s, s in acceptingStates), states_strings))

        # On ajoute chaque transition à son etat d'origine
        for state in states:
            state.transitions.extend(get_transition(state))
            if state.name == initial_state:
                self.initial_state = state


        if not self.is_deterministic():
            self._make_deterministic()
            if not self.is_deterministic():
                print('WARNING: Couldn\'t determinize automata')
    def deepcopy(self):
        transitions = list(chain(
            *map(lambda s: ((s.name, t[0], t[1].name) for t in s.transitions),
                 self.get_states())))
        initial_state = self.initial_state.name
        accepting_states = list(map(lambda s: s.name,
                                    filter(lambda s: s.accepting, self.get_states())))
        return Automata(transitions, initial_state, accepting_states)

    @staticmethod
    def from_string(string: str):
        transitions = [tuple(line.split()) for line in string.split('\n')[:-1]]
        accepting_states = string.split('\n')[-1][2:].split()
        return Automata(transitions, transitions[0][0], accepting_states)
    # Returns an automata with a single and accepting state
    @staticmethod
    def epsilon():
        automata = Automata([('0', '', '0')], '0', ['0'])
        return automata
    def __str__(self):
        return '\n'.join(map(str, self.get_states()))

    def get_state_by_name(self, state_name: str):
        for state in self.get_states():
            if state.name == state_name:
                return state
    def get_states(self):
        states = [self.initial_state]
        for state in states:
            yield state
            for _, next_state in state.transitions:
                if next_state not in states:
                    states.append(next_state)
    def normalize_names(self):
        #On renomme les etats
        new_names = dict(zip(self.get_states(), map(str, count())))
        for state in self.get_states():
            state.name = new_names[state]


    ######################################
    #                                    #
    #            --- TP 1 ---            #
    #                                    #
    ######################################

    # PS: Toutes les transitions X vers X via epsilon ont déjà été supprimées dans __init__
    def is_deterministic(self):
        for state in self.get_states():
            # On itere sur chaque transition pour chaque symbole
            for symbol, transitions in groupby(sorted(t[0] for t in state.transitions)):
                if symbol == '%' or len(list(transitions)) > 1: return False
        return True
    def is_recognized(self, word: str):
        state = self.initial_state
        for symbol in word:
            if symbol == '%': continue
            if state: state = state.get_next_state(symbol)
        return state != None and state.accepting

    ######################################
    #                                    #
    #            --- TP 2 ---            #
    #                                    #
    ######################################

    def _make_deterministic(self):

        # Remove epsilons

        for state in self.get_states():
            seen = [] # Necessary to avoid inifite loops in some cases
            def get_transitions(s):
                seen.append(s)
                state.accepting = state.accepting or s.accepting
                for t in s.transitions:
                    if t[0] != '%': yield t
                    elif t[1] not in seen: yield from get_transitions(t[1])
            state.transitions = set(get_transitions(state))

        # Reduce transitions
        # On appelera un 'superetat' une superposition de plusieurs etats

        def hash_superstate(superstate):
            # We use str(hash(s)) so that we don't even need to worry about conflicting names
            return str(hash(''.join(map(lambda s: str(hash(s)), superstate))))

        states = [set([self.initial_state])]
        initial_state_hash = hash_superstate(states[0])
        accepting_states_hashes = []
        transitions = []

        for superstate in states:
            superstate_hash = hash_superstate(superstate)
            key = lambda t: t[0]; to_transi = lambda s: s.transitions
            reachable_states_per_symbol = groupby(sorted(chain(*map(to_transi, superstate)),
                                                         key=key), key)

            # On verifie si le superetat est acceptant (si un seul de ses sous etats l'est)
            if any(map(lambda s: s.accepting, superstate)):
                accepting_states_hashes.append(superstate_hash)

            # Pour chaque superetat qu'on peut atteindre depuis l'actuel,
            # On l'ajoute à states si il n'y est pas deja
            # Puis on ajoute une transition vers le nouveau superetat
            for symbol, s in reachable_states_per_symbol:
                new_superstate = set(map(lambda s: s[1], s))
                new_superstate_hash = hash_superstate(new_superstate)

                if new_superstate not in states: states.append(new_superstate)
                transitions.append((superstate_hash, symbol, new_superstate_hash))

        # On remplace notre automate par le nouveau
        new_automata = Automata(transitions, initial_state_hash, accepting_states_hashes)
        self.initial_state = new_automata.initial_state

        self.normalize_names()

    ######################################
    #                                    #
    #            --- TP 3 ---            #
    #                                    #
    ######################################

    # Note: on ne normalise pas les noms car _make_deterministic le fait deja
    # Aussi, les noms pris au hasard ne posent pas probleme apres normalisation

    # Returns a new automata, doesn't change self's state
    def kleene(self):
        automata = self.deepcopy()
        for state in filter(lambda s: s.accepting, automata.get_states()):
            state.transitions.append(('%', automata.initial_state))

        new_initial_state = Automata.State(str(hash(23473842784)), True)
        new_initial_state.transitions = [('%', automata.initial_state)]
        automata.initial_state = new_initial_state

        automata._make_deterministic()
        return automata

    def concat(self, oth):
        automata = self.deepcopy()
        other = oth.deepcopy()
        # La conversion en list est très importante!
        # Sinon le generateur get_states s'adapte et renvoie les etats qu'on vient d'ajouter
        for s in list(filter(lambda s: s.accepting, automata.get_states())):
            s.transitions.append(('%', other.initial_state))
            s.accepting = False
        automata._make_deterministic()
        return automata
    
    def union(self, oth):
        automata = self.deepcopy()
        other = oth.deepcopy()
        new_initial_state = Automata.State(str(hash(98439832)), False)
        new_initial_state.transitions = [('%', automata.initial_state), ('%', other.initial_state)]
        automata.initial_state = new_initial_state
        automata._make_deterministic()
        return automata
