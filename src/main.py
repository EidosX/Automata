from Automata import *

#source = """0 a 1
#0 b 2
#1 a 1
#2 b 2
#A 0 1 2
#"""

source = """1 a 2
2 b 3
3 a 3
3 b 3
A 3
"""

word = "aaabb"

a = Automata(source)
print(a.isAccepted("abaabbab"))
