class DFA():
    """
    Represents a Deterministic Finite Automaton (DFA).

    Attributes:
        states (list): List of states in the DFA.
        alphabet (list): List of symbols in the alphabet of the DFA.
        initial_state (str): The initial state of the DFA.
        acceptance_states (list): List of acceptance states in the DFA.
        mapping (dict): Dictionary representing the transition mapping of the DFA.

    Methods:
        __init__(states, alphabet, initial_state, acceptance_states, mapping):
            Initializes a new instance of the DFA class.
        __repr__():
            Returns a string representation of the DFA.
        simulate(input):
            Simulates the DFA on the given input string.

    """
    def __init__(self, states, alphabet, initial_state, acceptance_states, mapping):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.acceptance_states = acceptance_states
        self.mapping = mapping


    def __repr__(self):
        dfa_str = "DFA(\n"
        dfa_str += f"\tstates={self.states},\n"
        dfa_str += f"\talphabet={self.alphabet},\n"
        dfa_str += f"\tinitial_state={self.initial_state},\n"
        dfa_str += f"\tacceptance_states={self.acceptance_states},\n"
        dfa_str += f"\tmapping={self.mapping}\n"
        dfa_str += ")"
        return dfa_str


    def simulate(self, input):
        """
        Simulates the DFA by processing the given input string.

        Args:
            input (str): The input string to be processed by the DFA.

        Returns:
            tuple: A tuple containing a boolean value indicating whether the input was accepted by the DFA,
                   and an integer representing the token associated with the final state.

        """

        # get current state
        current_state = self.initial_state

        for symbol in input:
            current_transition = self.mapping.get(current_state, False)

            if (current_transition == False):
                return False, 0

            current_state = current_transition.get(symbol, False)

            if ((type(current_state) == bool) and (current_state == False)):
                return False, 0

        # New final states for dfa withou tokens
        actual_acceptance_states = [state[0] for state in self.acceptance_states]

        # Return token if the state is in the acceptance states
        for state in self.acceptance_states:
            if (state[0] == current_state):
                return True, state[1][1]

        # Return if the state is in the acceptance states
        return current_state in actual_acceptance_states, current_state