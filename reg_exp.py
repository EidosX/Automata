from automata import Automata

def infix_to_postfix(in_expr):
    operator_priority = {
        '+': 1,
        '.': 2,
        '*': 3
    }
    isOperator = lambda x: x in operator_priority

    # On ajoute explicitement les operateurs de concatenation
    expression = ''
    for prev, char in zip(in_expr[:-1], in_expr[1:]):
        expression += prev
        if prev != '*' and isOperator(prev) or isOperator(char):
            continue
        if prev == '(' or char == ')':
            continue
        expression += '.'
    expression += in_expr[-1]

    # L'algo de conversion commence ici

    stack = []
    postfix = ''

    for symbol in expression:
        if symbol == ')':
            # Si une parenthese se ferme on pop tout ce qu'il y a entre parentheses
            while stack[-1] != '(':
                postfix += stack.pop()
            stack.pop()
        elif symbol == '(':
            stack.append(symbol)
        elif isOperator(symbol):
            # Si on tombe sur un operateur, on doit le mettre dans le stack
            # Mais on doit d'abord s'assurer qu'il ne soit pas à coté d'un operateur
            # Ayant une priorité plus grande ou identique
            op_priority = operator_priority[symbol]
            while len(stack) > 0 and isOperator(stack[-1]) and operator_priority[stack[-1]] >= op_priority:
                postfix += stack.pop()
            stack.append(symbol)
        else:
            # Tous les autres symboles vont directement dans la string
            postfix += symbol
    # On vide les operateurs encore dans le stack
    while len(stack):
        postfix += stack.pop()
    return postfix


######################################
#                                    #
#            --- TP 4 ---            #
#                                    #
######################################

def is_recognized(reg_exp : str, word : str):
    def isOperation(char): return char in ['*', '+', '.']
    def performOperation(stack, char):
        if char == '*': stack[-1] = stack[-1].kleene()
        elif char == '+':
            a, b = stack.pop(), stack.pop()
            stack.append(a.union(b))
        elif char == '.':
            r, l = stack.pop(), stack.pop()
            stack.append(l.concat(r))
            
            

    stack = []
    for char in infix_to_postfix(reg_exp):
        if not isOperation(char):
            if char == '%':
                stack.append(Automata.epsilon())
            else:
                stack.append(Automata([('1',char,'2')], '1', ['2']))
        else: performOperation(stack, char)
    if len(stack) != 1: raise IndexError("Invalid regular expression")
    return stack[0].is_recognized(word)

