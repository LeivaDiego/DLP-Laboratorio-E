def simulate_yalex_file(path, output_file, dfa, output_type, return_token):
    """
    Simulates a YALEX file given a path to the file, a DFA (Deterministic Finite Automaton),
    an output file path, an output type, and a function to return the token.

    Parameters:
    - path (str): The path to the YALEX file to be simulated.
    - output_file (str): The path to the output file where the simulation results will be written.
    - dfa (DFA): The DFA (Deterministic Finite Automaton) used for the simulation.
    - output_type (str): The type of output to generate. Can be "analysis" or "parsing".
    - return_token (function): A function that takes a found token and returns the corresponding token.

    Returns:
    None
    """
    file_string = ""

    output_file_lines = []

    # testing file reading
    with open(path, "r", newline="") as file:
        for line in file:
            for char in line:
                file_string += char

    # from string to ascii code
    file_string = [str(ord(char)) for char in file_string if (ord(char) != 13)]

    i, j = 0, 0
    MAX_LOOK_AHEAD = 3
    iteration = 0
    file_string_length = len(file_string)

    while (len(file_string) > 0):
        if (iteration > (5 * file_string_length)):
            break

        if (j < len(file_string)):
            simulated_string = [file_string[j]]
        else:
            break

        result, found_token = dfa.simulate(simulated_string)
        token = return_token(found_token)

        look_ahead = 1

        # Lexycal error for refused character
        if (not result):
            output_file_lines.append(f"ERROR:{''.join([chr(int(char)) for char in simulated_string])}\n")
            i += 1
            j = i

        while (result):
            last_token = token

            result, found_token = dfa.simulate(simulated_string)
            token = return_token(found_token)

            if (result):
                i += 1 if (len(file_string) > 1) else 0

                if (i < len(file_string)):
                    simulated_string.append(file_string[i])
                else:
                    simulated_string.append(file_string[0])

                if (len(file_string) == 1):

                    output_file_lines.append(f"{last_token}:{''.join([chr(int(char)) for char in simulated_string[:-1]])}\n")
                    file_string = []
                    break

            else:
                string_before_look_ahead = simulated_string.copy()

                while ((look_ahead <= MAX_LOOK_AHEAD) and ((i + look_ahead) < len(file_string))):

                    look_ahead_simulated_string = simulated_string + [file_string[i + look_ahead]]
                    look_ahead_result, found_look_ahead_token = dfa.simulate(look_ahead_simulated_string)
                    look_ahead_token = return_token(found_look_ahead_token)
                    simulated_string = look_ahead_simulated_string.copy()

                    if (look_ahead_result):
                        result = look_ahead_result
                        token = look_ahead_token
                        i += look_ahead
                        look_ahead = 1
                        break
                    else:
                        look_ahead += 1

                else:
                    output_file_lines.append(f"{last_token}:{''.join([chr(int(char)) for char in string_before_look_ahead[:-1]])}\n")
                    file_string = file_string[i:]
                    i, j = 0, 0
                    if (len(file_string) == 0):
                        break
                    simulated_string = [file_string[0]] if (j > (len(file_string) - 1)) else [file_string[j]]
                    break

            iteration += 1

            if (iteration >  (5 * file_string_length)):
                break

    # Output file generation with the simulation results
    with open(output_file, "w", newline="\n") as file:
        if (output_type == "analysis"):
            file.write(f"- * - * - \"{path}\" simulation results: - * - * -\n\n")
            for line in output_file_lines:
                file.write(line)
        elif (output_type == "parsing"):
            for line in output_file_lines:
                splitted_line = line.split(":")
                token_to_write = splitted_line[0]
                if (token_to_write == "WHITESPACE"):
                    continue
                file.write(token_to_write + " ")

    print(f"\nFile simulation succes. Tokens in: \"{output_file}\".\n")
