Nom: Diego IMBERT (pas de binome)
Lien depot git: https://github.com/RedRikudo/AutomatesTP1

Dependances: itertools, sys, os (normalement tous natifs à python3).
Utilisation: ./tp4automates.py {regular_expression} {word_to_recognize}
             Les parenthèses doivent être échappées comme ceci: \(mon_expression\)
             Exemple: ./tp4automates.py \(ab+c*\)a\(bca\)* ababcabca

- Le programme est ecrit en python 3.
- Le TP 1, 2 et 3 sont dans automata.py mais le tp4 est dans reg_exp.py.
  De gros indicateurs sont en commentaires pour les reperer.

Tout a été refait a partir du TP 3.
Les anciennes versions sont toujours présentes dans les commits du github.

Inspirations / Tutoriels suivis:
  - https://youtube.com/watch?v=Qu3dThVy6KQ (itertools)
  - https://youtube.com/watch?v=vXPL6UavUeA (conversion infix / postfix)