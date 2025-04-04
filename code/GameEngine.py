import copy
from UI import *
import pygame



ALPHACOLS = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U'}


def CreateMatrix(rows: int, cols: int):
    Matrix = [[(0,0) for x in range(cols)] for y in range(rows)]
    return Matrix


def valid_position(row, col):
    return 0 <= row < DIM and 0 <= col < DIM 


def empty_position(stack):
    if len(stack) == 0: return True
    else: return False


def has_pawn_at(stack, position):
    if position < 0 or position >= len(stack):
        return False  
    return bool(stack[position])

def char_to_int(col):
    REVERSE_ALPHACOLS = {v: k for k, v in ALPHACOLS.items()}
    return REVERSE_ALPHACOLS[col]

def move_with_input(x, y, z, move):
    # provera X
   
    while True:
        x = input("Unesite prvu poziciju polja (A-H): ").upper()
        while(x not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
            x = input("Neispravan unos, unesite poziciju polja (A-H): ").upper()
        x = char_to_int(x)
        while True:
            try:
                y = int(input("Unesite drugu poziciju polja (1-8): ")) - 1 
                break  
            except ValueError:
                print("Molimo unesite celobrojnu vrednost 1-8.")
        if valid_position(x, y):
            try:
                dict = stack_dictionary[(x, y)]
                while empty_position(dict):
                    print("Na unetoj poziciji ne postoji figura.")
                    x = input("Unesite poziciju polja (A-H): ").upper()
                    y = int(input("Unesite poziciju polja (1-8): ")) - 1
                    x = char_to_int(x)
                    dict = stack_dictionary[(x, y)]
                break
            except KeyError:
                print("Na belim pozicijama ne nalaze se figure. Ponovite unos.")
        else:
            print("Nije uneta validna pozicija.")

        

    # provera Z
    while True:
        try:
            z = int(input("Unesite poziciju figure na steku: "))
            if has_pawn_at(dict, z):
                break 
            else:
                print("Na unetoj poziciji ne postoji figura, unesite ponovo.")
        except ValueError:
            print("Neispravan unos. Molimo unesite celobrojnu vrednost.")

    # provera POTEZ
    move = input("Unesite smer kretanja figure: ").upper()
    while(move not in ['GD', 'GL', 'DL', 'DD']):
        move = input("Unesite pravac kretanja (GD, GL, DL, DD): ").upper()
    if move == 'GD':
        valid_position(x + 1, y - 1)
    elif move == 'GL':
        valid_position(x - 1 , y - 1)
    elif move == 'DL':
        valid_position(x - 1 , y + 1)
    elif move == 'DD':
        valid_position(x + 1 , y + 1)
    else:
        print("Zeljeni potez nije moguce odigrati!")

    return (x, y, z, move)
    


def odigraj_potez(x, y, z, move):
    if (x, y) in stack_dictionary and len(stack_dictionary[(x, y)]) > z:
        figures_to_move = stack_dictionary[(x, y)][z:]
        
        move = move_to_coords(move)

        # dodavanje figura na novu poziciju 
        if (x+move[0], y+move[1]) in stack_dictionary:
            stack_dictionary[(x+move[0], y+move[1])].extend(figures_to_move)
        else:
            stack_dictionary[(x+move[0], y+move[1])] = figures_to_move
        
        # uklanjanje figura sa prvobitnog steka
        stack_dictionary[(x, y)] = stack_dictionary[(x, y)][:z]

#  realizovati funkcije koje proveravaju da li su susedna polja prazna
#  x, y -> (x-1, y-1) GL, (x-1, y+1) GD, (x+1, y-1) DL, (x+1, y+1) DD
def empty_neighbours(x, y):
    coords = [(x-1,y-1), (x-1,y+1), (x+1,y-1), (x+1,y+1)]
    for c in coords:
        if valid_position(c[0], c[1]):
            if len(stack_dictionary[c]) != 0:
                return True
    return False

#  realizovati funkcije koje na osnovu konkretnog poteza i stanje igre 
#  proveravaju da li on vodi ka jednom od najbližih stekova (figura)
#  vraca smer koji vodi do nablizeg steka
def find_nearest_stack(stack_dict, x, y):
    visited = set()
    queue = [(x, y, 0, (0, 0))]
    closest = set()
    min_jumps = float('inf')

    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for current_row, current_col, jumps, start_direction in queue:
        visited.add((current_row, current_col))

        if (current_row, current_col) in stack_dict and stack_dict[(current_row, current_col)] and start_direction != (0, 0):
            if jumps < min_jumps:
                closest = {(start_direction)}
                min_jumps = jumps
            elif jumps == min_jumps:
                closest.add(start_direction)

        for direction in directions:
            new_row, new_col = current_row + direction[0], current_col + direction[1]
            new_direction = direction if start_direction == (0, 0) else start_direction

            if valid_position(new_row, new_col) and (new_row, new_col) not in visited:
                queue.append((new_row, new_col, jumps + 1, new_direction))

    return list(closest)

#da l se pribliziva do najblizi stek
def valid_stack_move(stack_dict, x, y, smer):
    has_neighbours = empty_neighbours(x, y)
    nearest_stack_direction = find_nearest_stack(stack_dict, x, y)
    for s in nearest_stack_direction:
        if smer == s and (not has_neighbours or has_neighbours):
            return True

    return False

# KRAJ IGRE
def game_over(player_x, player_o):
    if(player_x == STACK_NUM - 1 or player_o == STACK_NUM - 1):
       return True
    return False

# smena poteza izmedju igraca
def change_player(player):
    if(player == 'X'):
        player = 'O'
    else:
        player = 'X'
    return player

#  realizovati funkcije koje na osnovu konkretnog poteza i stanja igre 
#  proveravaju da li se potez može odigrati prema pravilima pomeranja 
#  definisanim za stekove
def check_move(stack_d, x, y, z, move, starting_player):
    move_coords = move_to_coords(move)
    # da li izlazi iz okvira table
    stack = stack_d[(x, y)]
    if not valid_position(x, y):
        return False
    # da li je polje prazno
    if empty_position(stack):
        return False
    # da li postoji figura na toj poziciji
    if not has_pawn_at(stack, z):
        return False
    # X = crne, O = bele
    # provera figura
    if starting_player == 'X' and stack_d[(x, y)][z] != (0, 0, 0):
        return False
    if starting_player == 'O' and stack_d[(x, y)][z] != (255, 255, 255):
        return False
    # move_coords = koordinate polja zeljenog poteza
    # provera validnosti poteza prema pravilima igre

    #da li odigrani potez izlazi van opsega tabele
    if not valid_position(x + move_coords[0], y + move_coords[1]):
        return False
    

    if not empty_position(stack_d[(x + move_coords[0], y + move_coords[1])]):
        # provera da li se figura premesta na istu ili nizu visinu
        if len(stack_d[(x + move_coords[0], y + move_coords[1])]) <= z:
            return False
        # provera da li je ce stek biti > 8 nakon poteza 
        if (len(stack_d[( x + move_coords[0], y + move_coords[1])]) + len(stack) - z) > 8:
            return False
        return True
    
    if z != 0 and len(stack_d[x + move_coords[0], y + move_coords[1]]) == 0:
       return False

    if valid_stack_move(stack_d, x, y, move_coords) == False:
        return False
    else:
        return True

   
    
# x, y -> (x-1, y-1) GL, (x-1, y+1) GD, (x+1, y-1) DL, (x+1, y+1) DD
def move_to_coords(move):
    move_c = tuple()
    if move == "DD":
        move_c = (1, 1) 
    if move == "DL":
        move_c = (1, -1)
    if move == "GD":
        move_c = (-1, 1)
    if move == "GL":
        move_c = (-1, -1)
    return move_c


def look_for_stacks(stack_dictionary, p_x, p_o):
    stacks_to_remove = [] 

    for key in stack_dictionary.keys():
        if len(stack_dictionary[key]) == 8:
            last = stack_dictionary[key][-1]
            if last == (0, 0, 0):
                p_x += 1
                print("X je osvojio poen!")
            else:
                p_o += 1
                print("O je osvojio poen!")
            stacks_to_remove.append(key)

    for key in stacks_to_remove:
        stack_dictionary[key] = stack_dictionary[key][:0]
    print("X: ", p_x, " O: ", p_o)
    return (p_x, p_o)


def update(win):
    tabla(win)
    pygame.display.update()


def operator(stack, player):
    target_value = (0, 0, 0) if player == 'X' else (255, 255, 255)
    possible_moves = []
    direction = ["DD", "DL", "GD", "GL"]
    for keys in stack.keys():
        if len(stack[keys]) != 0:
            for index, item in enumerate(stack[keys]):
                if item == target_value:
                    # izvrsiti proveru poteza
                    for d in direction:
                        x, y = keys
                        if check_move(stack, x, y, index, d, player):
                            possible_moves.append((x, y, index, d))
    
    return possible_moves

         

def potezv2(x, y, z, move, stack):
    if (x, y) in stack and len(stack[(x, y)]) > z:
        figures_to_move = stack[(x, y)][z:]
        
        move = move_to_coords(move)

        # dodavanje figura na novu poziciju 
        if (x+move[0], y+move[1]) in stack:
            stack[(x+move[0], y+move[1])].extend(figures_to_move)
        else:
            stack[(x+move[0], y+move[1])] = figures_to_move
        
        # uklanjanje figura sa prvobitnog steka
        stack[(x, y)] = stack[(x, y)][:z]


def odigraj(stack, s, starting_player):
    if check_move(stack, s[0], s[1], s[2], s[3], starting_player):
        updated_stack = copy.deepcopy(stack)
        potezv2(s[0], s[1], s[2], s[3], updated_stack)
        return updated_stack
    
    return stack



