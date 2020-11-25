from Automata import *
from AutomataMakeDeterministic import *
import sys
import os

if len(sys.argv) != 3:
    print("Error: invalid format. \nUsage: ./automata filename.txt wordtofind")
    sys.exit(0)
if not os.path.exists(sys.argv[1]):
    print("Error: file does not exist")
    sys.exit(0)
if not os.path.isfile(sys.argv[1]):
    print("Error: first argument must be a path to a file")
    sys.exit(0)

with open(sys.argv[1], 'r') as file:
    source = file.read()
word = sys.argv[2]

automata = textToAutomata(source)
if (not automata.isDeterministic()):
    automata = makeDeterministic(automata)
print("YES" if automata.isAccepted(word) else "NO")
