from Automata import *
import sys
import os
def print_and_exit(str): print(str); sys.exit(-1)

# On verifie les erreurs evidentes de l'utilisateur
if (len(sys.argv) != 3):            print_and_exit('Usage: ./automata \'path_to_file.af\' \'word_to_find\'')
if not os.path.exists(sys.argv[1]): print_and_exit("Error: file does not exist")
if not os.path.isfile(sys.argv[1]): print_and_exit("Error: first argument must be a path to a file")

# On lit le fichier et le mot à trouver
with open(sys.argv[1], 'r') as file: source = file.read()
word = sys.argv[2]

#On crée l'automate a partir du fichier
try: automata = Automata.from_string(source)
except (ValueError, IndexError): print_and_exit('Invalid automata')

osef = Automata.from_string("""1 1 2
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
A 4""")

print(f'recognized: {automata.union(osef).isRecognized(word) and "YES" or "NO"}')