from GameEngine import *

'''Ova pravila uzimaju u obzir boju i raspored figura u steku, dodeljujući bodove u skladu s tim, 
sa ciljem da se favorizuju pozicije gde su boje figura povoljne za trenutnog igrača. '''
def oceni(stanje, trenutni_igrac):
    vrednost_heuristike = 0
    target_value = (255, 255, 255) if trenutni_igrac == 'O' else (0, 0, 0)

    for stek in stanje.values():
        if stek:
            if len(stek) == 8: 
                if stek[-1] == target_value: return 1000
                else: return -1000 
                
            if stek[0] == target_value: 
                vrednost_heuristike += 5
                if stek[-1] == target_value: vrednost_heuristike += 10  
            else: vrednost_heuristike -= 5

            if stek[-1] == target_value: vrednost_heuristike += 5     
            else: vrednost_heuristike -= 5

    return vrednost_heuristike


def max_value(stanje, dubina, trenutni_igrac, alfa, beta, potez=None):
    
    lista_poteza = list(operator(stanje, trenutni_igrac))
    if dubina == 0 or lista_poteza is None or len(lista_poteza) == 0:
        return (potez, oceni(stanje, trenutni_igrac))
    else:
        for s in lista_poteza:
                novo_stanje = odigraj(stanje, s, trenutni_igrac)
                res = min_value(novo_stanje, dubina - 1, 'O', alfa, beta, s if potez is None else potez)
                if res[1] > alfa[1]:
                    alfa = (s if potez is None else potez, res[1])
                if alfa[1] >= beta[1]:
                    return beta
        return alfa

def min_value(stanje, dubina, trenutni_igrac, alfa, beta, potez=None):
   
    lista_poteza = list(operator(stanje, trenutni_igrac))
    if dubina == 0 or lista_poteza is None or len(lista_poteza) == 0:
        return (potez, oceni(stanje, trenutni_igrac))
    else:
        for s in lista_poteza:
                novo_stanje = odigraj(stanje, s, trenutni_igrac)
                res = max_value(novo_stanje, dubina - 1, 'X', alfa, beta, s if potez is None else potez)
                if res[1] < beta[1]:
                    beta = (s if potez is None else potez, res[1])
                if beta[1] <= alfa[1]:
                    return alfa
        return beta


def min_max(inic_stanje, dubina, moj_potez, trenutni_igrac, alpha = (None, float('-inf')), beta = (None, float('inf'))):
    stanje = copy.deepcopy(inic_stanje)
    if moj_potez:
        return max_value(stanje, dubina, trenutni_igrac, alpha, beta)
    else:
        return min_value(stanje, dubina, trenutni_igrac, alpha, beta)



