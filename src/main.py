import sys
import os
from automata import Automata

def print_and_exit(message):
    print(message)
    sys.exit(-1)

# On verifie les erreurs evidentes de l'utilisateur
if len(sys.argv) != 3:
    print_and_exit('Usage: ./automata \'path_to_file.af\' \'word_to_find\'')
if not os.path.exists(sys.argv[1]):
    print_and_exit("Error: file does not exist")
if not os.path.isfile(sys.argv[1]):
    print_and_exit("Error: first argument must be a path to a file")

# On lit le fichier et le mot à trouver
with open(sys.argv[1], 'r') as file:
    SOURCE = file.read()
WORD = sys.argv[2]

#On crée l'automate a partir du fichier
try:
    AUTOMATA = Automata.from_string(SOURCE)
except (ValueError, IndexError):
    print_and_exit('Invalid automata')

print(f'recognized: {AUTOMATA.kleene().is_recognized(WORD) and "YES" or "NO"}')
print(AUTOMATA)