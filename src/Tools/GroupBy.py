# Renvoie un dictionnaire
def groupBy(keyFun, valueFun, list):
    dictionnary = dict()
    for t in list:
        symbol = keyFun(t)
        state = valueFun(t)
        if symbol not in dictionnary:
            dictionnary[symbol] = []
        dictionnary[symbol].append(state)
    return dictionnary